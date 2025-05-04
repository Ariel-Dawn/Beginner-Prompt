import zipfile
import os

project_name = "VoiceImageEditor"
zip_filename = f"{project_name}.zip"

# File contents
project_files = {
    f"{project_name}/voice_image_editor.py": """
import speech_recognition as sr
from PIL import Image, ImageFilter
import cv2
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        speak(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
    except sr.RequestError:
        speak("Speech service error.")
    return ""

def process_image(command, image_path='sample.jpg'):
    try:
        image = Image.open(image_path)
        cv_image = cv2.imread(image_path)
        output_path = 'output.jpg'

        if "rotate" in command:
            image = image.rotate(90)
            image.save(output_path)
            speak("Image rotated.")
        elif "grayscale" in command or "gray" in command:
            image = image.convert('L')
            image.save(output_path)
            speak("Image converted to grayscale.")
        elif "blur" in command:
            blurred = cv2.GaussianBlur(cv_image, (15, 15), 0)
            cv2.imwrite(output_path, blurred)
            speak("Image blurred.")
        elif "resize" in command:
            image = image.resize((200, 200))
            image.save(output_path)
            speak("Image resized to 200x200.")
        elif "flip" in command:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            image.save(output_path)
            speak("Image flipped horizontally.")
        else:
            speak("Command not recognized. Try rotate, grayscale, blur, resize, or flip.")
            return

        speak("Edit complete. Saved as output.jpg.")

    except Exception as e:
        speak(f"Error processing image: {str(e)}")

def main():
    command = get_voice_command()
    if command:
        process_image(command)

if __name__ == "__main__":
    main()
""",

    f"{project_name}/requirements.txt": """
speechrecognition
pyaudio
opencv-python
pillow
pyttsx3
""",

    f"{project_name}/README.md": """
# Voice Image Editor

Edit images using voice commands like "rotate", "grayscale", or "blur". Built using Python, OpenCV, Pillow, and Google Speech Recognition.

## Features

- Voice-controlled image editing
- Supported commands:
  - Rotate
  - Grayscale
  - Blur
  - Resize
  - Flip horizontally

## How to Use

1. Place an image named `sample.jpg` in the same directory.
2. Run the script:

```bash
python voice_image_editor.py
pip install -r requirements.txt
sudo apt install portaudio19-dev python3-pyaudio
