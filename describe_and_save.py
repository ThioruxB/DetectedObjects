import os
import subprocess
import json
import glob
import csv
import sys

def describe_and_save(api_key):
    cropped_persons_dir = "cropped_persons"
    json_results = []

    if not os.path.exists(cropped_persons_dir):
        print(f"Error: Directory '{cropped_persons_dir}' not found.")
        return

    image_files = sorted(glob.glob(os.path.join(cropped_persons_dir, "person_*.jpg")))[:10]
    if not image_files:
        print(f"No cropped images found in '{cropped_persons_dir}'.")
        return

    print(f"Processing {len(image_files)} cropped images...")
    for image_file in image_files:
        print(f"Describing person in: {image_file}")
        describe_command = ["D:\\YOLO\\venv\\Scripts\\python.exe", "describe_person.py", api_key, image_file]
        try:
            result = subprocess.run(describe_command, capture_output=True, text=True, check=True, encoding='utf-8')
            json_output = result.stdout.strip()
            try:
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

    output_json_file = "results.json"
    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(json_results, f, ensure_ascii=False, indent=2)
    print(f"All results saved to {output_json_file}")

    if not json_results:
        print("No results to convert to CSV.")
        return

    output_csv_file = "results.csv"
    if json_results and 'description' in json_results[0] and json_results[0]['description']:
        first_description = json_results[0]['description']
        headers = ['image'] + list(first_description.keys())

        with open(output_csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for item in json_results:
                row = {'image': item['image']}
                if 'description' in item and item['description']:
                    row.update(item['description'])
                writer.writerow(row)

        print(f"CSV file saved to {output_csv_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key_arg = sys.argv[1]
        describe_and_save(api_key_arg)
    else:
        print("Please provide the API key as a command-line argument.")