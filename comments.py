import time
import pytchat
import requests
from datetime import datetime

API_DOMAIN  = ""
STREAM_ID   = ""

def console_msg(message, color='white'):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    colors = {
        'white': '\x1b[37m',
        'yellow': '\x1b[33m',
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'pink': '\x1b[35m',
        'cyan': '\x1b[38;5;51m'
    }
    text_color = colors.get(color, colors['white'])
    print(f'\x1b[36m{formatted_date}\x1b[0m {text_color}{message}\x1b[0m')

def send_scenario(requestor_name, topic_text):
    try:
        payload = {
            "author": requestor_name,
            "topic": topic_text,
        }

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        response = requests.post(
            f"https://{API_DOMAIN}/submit.php",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            console_msg(f"Сценарий от пользователя '{requestor_name}' успешно отправлен в БД.", 'green')
        else:
            console_msg(f"Ошибка при отправке сценария. Статус: {response.status_code}", 'red')
            print(response.text)
    except Exception as e:
        console_msg("Исключение при отправке сценария:", 'red')
        print(e)

def main():
    while True:
        try:
            chat = pytchat.create(video_id=STREAM_ID)
            while chat.is_alive():
                try:
                    for c in chat.get().sync_items():
                        console_msg(f"[{c.author.name}]: {c.message}")

                        if c.message.startswith("/тема"):
                            topic_text = c.message[len("/тема"):].strip()
                            if topic_text:
                                send_scenario(c.author.name, topic_text)

                except Exception as e:
                    console_msg(f"Ошибка при получении сообщений чата: {e}", 'red')
                    time.sleep(5)
                    break
        except Exception as e:
            console_msg(f"Ошибка при создании объекта чата: {e}", 'red')
            time.sleep(5)

if __name__ == "__main__":
    main()