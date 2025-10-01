import os
import subprocess
import json
import glob

def run_detection_and_description(video_path):
    # Step 1: Run detect.py to get cropped images
    print(f"Running detect.py for video: {video_path}")
    detect_command = ["python", "detect.py", video_path]
    try:
        subprocess.run(detect_command, check=True)
        print("detect.py finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running detect.py: {e}")
        return

    # Step 2: Process each cropped image with describe_person.py
    cropped_persons_dir = "cropped_persons"
    json_results = []

    if not os.path.exists(cropped_persons_dir):
        print(f"Error: Directory '{cropped_persons_dir}' not found.")
        return

    image_files = glob.glob(os.path.join(cropped_persons_dir, "*.jpg"))
    if not image_files:
        print(f"No cropped images found in '{cropped_persons_dir}'.")
        return

    print(f"Processing {len(image_files)} cropped images...")
    for image_file in image_files:
        print(f"Describing person in: {image_file}")
        describe_command = ["D:\\YOLO\\venv\\Scripts\\python.exe", "describe_person.py", image_file]
        try:
            result = subprocess.run(describe_command, capture_output=True, text=True, check=True)
            json_output = result.stdout.strip()
            try:
                # The model might output extra text before or after the JSON.
                # We need to extract only the JSON part.
                start_index = json_output.find('{')
                end_index = json_output.rfind('}') + 1
                if start_index != -1 and end_index != -1 and start_index < end_index:
                    json_str = json_output[start_index:end_index]
                    json_data = json.loads(json_str)
                    json_results.append({"image": os.path.basename(image_file), "description": json_data})
                else:
                    print(f"Warning: Could not find valid JSON in output for {image_file}: {json_output}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for {image_file}: {e}\nOutput: {json_output}")
        except subprocess.CalledProcessError as e:
            print(f"Error running describe_person.py for {image_file}: {e}\nStderr: {e.stderr}")

    # Step 3: Save all JSON results to a single file
    output_json_file = "results.json"
    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(json_results, f, ensure_ascii=False, indent=2)
    print(f"All results saved to {output_json_file}")

if __name__ == "__main__":
    video_to_process = "video.mp4"
    if not os.path.exists(video_to_process):
        print(f"Error: Video file '{video_to_process}' not found in the current directory.")
    else:
        run_detection_and_description(video_to_process)