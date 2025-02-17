import sys
import time
import os
import requests
import random
import string
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

def print_colored_message(message):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[1;36m[{current_datetime}]\033[0m {message}")

speaker_map = {
    "gordon": "gordon.wav",
    "zhirinovskiy": "zhirinovskiy.wav"
}

@app.route('/generate_voice', methods=['POST'])
def generate_voice():
    try:
        input_text = request.json['text']
        input_speaker = request.json['speaker']
        
        if input_speaker in speaker_map:
            character_voice = speaker_map[input_speaker]
        else:
            character_voice = "zhirinovskiy.wav"
        
        print_colored_message(f"Озвучка диалога: [{input_speaker}] {input_text}")

        payload = {
            "text_input": input_text,
            "text_filtering": "standard",
            "character_voice_gen": character_voice,
            "narrator_enabled": "false",
            "narrator_voice_gen": "male_01.wav",
            "text_not_inside": "character",
            "language": "ru",
            "output_file_name": "alltalk_voice", 
            "output_file_timestamp": "true",
            "autoplay": "false",
            "autoplay_volume": "1.0"
        }

        url = "http://127.0.0.1:7851/api/tts-generate"
        response = requests.post(url, data=payload, timeout=60)
        response_json = response.json()

        if response_json.get("status") == "generate-success":
            audio_file_path = response_json.get("output_file_path", "")
            audio_file_url = response_json.get("output_file_url", "")
            return jsonify({'audio_wav_path': audio_file_path})
        else:
            return jsonify({'error': 'AllTalk TTS generate-failure'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)