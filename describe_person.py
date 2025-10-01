import google.generativeai as genai
import PIL.Image
import os
import sys
import json

def describe_person_from_image(api_key, image_path):
    try:
        genai.configure(api_key=api_key)
        img = PIL.Image.open(image_path)
    except FileNotFoundError:
        return json.dumps({{"error": f"Image file not found at {image_path}."}})
    except Exception as e:
        return json.dumps({{"error": f"Could not open image {image_path}: {e}"}})

    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt = "Proporcione la siguiente información sobre la persona en esta imagen en formato JSON, con las claves y los valores en español: rango de edad (mínima y máxima), género, descripción demográfica y perfil de consumidor (por ejemplo, deportista, tecnológico, etc.)."
    
    try:
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return json.dumps({{"error": f"An error occurred during content generation: {e}"}})

if __name__ == "__main__":
    if len(sys.argv) > 2:
        api_key_arg = sys.argv[1]
        image_file = sys.argv[2]
        print(describe_person_from_image(api_key_arg, image_file))
    else:
        print(json.dumps({{"error": "Please provide the API key and the path to the image file as arguments."}}))