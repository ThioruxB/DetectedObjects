
import cv2
from ultralytics import YOLO
import sys
import threading
import queue
import time
import numpy as np
import os
import imagehash
from PIL import Image

def object_detector(frame_queue, result_queue, stop_event):
    """Detects objects in frames from a queue and puts the results into another queue."""
    try:
        model = YOLO('yolov8m.pt')
        while not stop_event.is_set():
            try:
                frame = frame_queue.get(timeout=1)
                results = model.track(frame, imgsz=640, classes=0, conf=0.55, device='cuda', persist=True)
                result_queue.put(results)
            except queue.Empty:
                if frame_queue.qsize() == 0:
                    stop_event.set()
                continue
    except Exception as e:
        print(f"An error occurred in object detector: {e}")
    stop_event.set()

def detect_objects_in_video(video_path):
    """
    Detects objects in a video using the YOLO model with asynchronous processing.
    """
    frame_queue = queue.Queue(maxsize=2)
    result_queue = queue.Queue(maxsize=2)
    stop_event = threading.Event()

    detector_thread = threading.Thread(target=object_detector, args=(frame_queue, result_queue, stop_event))
    detector_thread.start()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    wait_time = int(1000 / fps)
    
    latest_results = None
    
    output_dir = "cropped_persons"
    os.makedirs(output_dir, exist_ok=True)

    all_detections = {}

    while cap.isOpened() and not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            stop_event.set()
            break

        if frame_queue.qsize() < 2:
            frame_queue.put(frame.copy())

        try:
            latest_results = result_queue.get_nowait()
        except queue.Empty:
            pass

        if latest_results is not None:
            annotated_frame = latest_results[0].plot()
            
            if latest_results[0].boxes is not None and hasattr(latest_results[0].boxes, 'id') and latest_results[0].boxes.id is not None:
                boxes = latest_results[0].boxes.xyxy.cpu().numpy().astype(int)
                ids = latest_results[0].boxes.id.cpu().numpy().astype(int)
                confs = latest_results[0].boxes.conf.cpu().numpy()

                for box, id, conf in zip(boxes, ids, confs):
                    x1, y1, x2, y2 = box
                    
                    padding = 30
                    y1_padded = max(0, y1 - padding)
                    y2_padded = min(frame.shape[0], y2 + padding)
                    x1_padded = max(0, x1 - padding)
                    x2_padded = min(frame.shape[1], x2 + padding)
                    crop = frame[y1_padded:y2_padded, x1_padded:x2_padded]

                    if crop.size == 0:
                        continue

                    if id not in all_detections:
                        all_detections[id] = []
                    
                    all_detections[id].append({
                        'image': crop,
                        'confidence': conf,
                        'area': (x2 - x1) * (y2 - y1)
                    })
        else:
            annotated_frame = frame

        cv2.imshow("YOLOv8 Inference", annotated_frame)
        
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break
    
    stop_event.set()
    detector_thread.join()
    cap.release()
    cv2.destroyAllWindows()

    best_crops = []
    for track_id in all_detections:
        best_crop_for_id = max(all_detections[track_id], key=lambda x: x['area'])
        best_crops.append(best_crop_for_id['image'])

    unique_hashes = []
    final_crops = []
    for crop in best_crops:
        crop_img = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        new_hash = imagehash.phash(crop_img)

        is_duplicate = False
        for h in unique_hashes:
            if new_hash - h < 10:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_hashes.append(new_hash)
            final_crops.append(crop)

    for i, crop in enumerate(final_crops):
        crop_filename = os.path.join(output_dir, f"person_{i + 1}.jpg")
        cv2.imwrite(crop_filename, crop)
        print(f"Saved unique person to {crop_filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_file = sys.argv[1]
        detect_objects_in_video(video_file)
    else:
        print("Please provide the path to the video file as an argument.")
        print("Usage: python detect.py <path_to_video>")
