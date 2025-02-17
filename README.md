![DEMO](demo.jpg)

# LATE NIGHT AI

LATE NIGHT AI is a software suite for running endless AI-powered livestreams. The system listens to YouTube chat for topics, generates dialogues between famous personalities using OpenAI, synthesizes voices, and displays synchronized video and subtitles.

## Features
- **YouTube Chat Integration** – Listens to user-submitted topics.
- **AI-Generated Dialogues** – Uses OpenAI to create dynamic conversations.
- **Voice Synthesis** – Converts generated text into speech.
- **Video Playback** – Displays pre-recorded footage in sync with AI-generated speech.
- **Web-Based Client** – Interactive interface with real-time subtitles and video.

## Installation
### Requirements
- Python 3.8+
- Node.js & npm
- PHP 7.4+
- MySQL or MariaDB
- Flask & aiohttp

### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/late-night-ai.git
cd late-night-ai
```

### 2. Set Up the Database
- Import the SQL dump:
```sh
mysql -u root -p < webserver/_database.sql
```
- Configure `webserver/dbconnect.php` with your database credentials.

### 3. Install Python Dependencies
```sh
pip install -r requirements.txt
```

### 4. Install Node.js Dependencies (if applicable)
```sh
cd client
npm install
```

### 5. Install AllTalk TTS
- Clone and install the AllTalk TTS system:
```sh
git clone https://github.com/erew123/alltalk_tts.git
cd alltalk_tts
pip install -r requirements.txt
```
- Move WAV files from `voices` directory to `alltalk_tts/voices`:
```sh
mv ../voices/*.wav alltalk_tts/voices/
```

### 6. Configure Environment Variables
Edit `controller.py` and `comments.py`, setting `API_DOMAIN` to your server's domain.

### 7. Run the Services
#### Start the Web Server
```sh
cd webserver
php -S 0.0.0.0:8080
```
#### Start the Python Backend
```sh
python3 gateway.py &
python3 controller.py &
python3 comments.py &
```

## Usage
1. Start the livestream.
2. Users submit topics in YouTube chat using `/topic <text>`.
3. AI generates a conversation based on the topic.
4. The system synthesizes voices and plays synchronized video.
5. The cycle repeats endlessly.

## License

This project is licensed under the MIT License.

## Contacts

Follow updates on the Telegram channel: [low digital](https://t.me/low_digital).
