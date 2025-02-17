import os
import asyncio
import aiohttp
import random
import time
import re
import json
from datetime import datetime
from aiohttp import web
import aiohttp_cors

API_DOMAIN  = ""
API_DEBUG   = True

generating = False

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

def contains_words_ignore_case(s, words):
    lower_s = s.lower()
    lower_words = [word.lower() for word in words]
    return any(word in lower_s for word in lower_words)

def get_random_int(max_value):
    return random.randrange(max_value)

async def wait(milliseconds):
    await asyncio.sleep(milliseconds / 1000)

def process_text(text):
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\*.*?\*', '', text)
    lines = text.split('\n')
    dialogue_list = []
    current_character = ''
    current_dialogue = ''
    for line in lines:
        line = line.strip()
        if line != '':
            colon_index = line.find(':')
            if colon_index != -1:
                current_character = line[:colon_index].strip()
                character_map = {
                    "Владимир Жириновский": "Владимир Жириновский",
                    "Жириновский": "Владимир Жириновский",
                    "жириновский": "Владимир Жириновский",
                    "владимир жириновский": "Владимир Жириновский",
                    "Дмитрий Гордон": "Дмитрий Гордон",
                    "Гордон": "Дмитрий Гордон",
                    "дмитрий гордон": "Дмитрий Гордон",
                    "гордон": "Дмитрий Гордон",
                }
                lowercase_character = current_character.lower()
                current_character = character_map.get(lowercase_character, current_character)
                current_dialogue = line[colon_index + 1:].strip().replace('"', '')
            else:
                current_dialogue += ' ' + line.replace('"', '')
            if current_dialogue != '':
                dialogue_list.append({
                    'character': current_character,
                    'dialogue': current_dialogue
                })
    return dialogue_list

async def request_voice(dialogue):
    console_msg(f'TTS: [{dialogue["character"]}] {dialogue["dialogue"]}')
    try:
        speaker_map = {
            "Владимир Жириновский": "zhirinovskiy",
            "Дмитрий Гордон": "gordon",
        }
        speaker = speaker_map.get(dialogue['character'], 'zhirinovskiy')
        data = {
            "text": dialogue['dialogue'],
            "speaker": speaker
        }
        async with aiohttp.ClientSession() as session:
            async with session.post("http://127.0.0.1:3000/generate_voice", json=data) as response:
                json_response = await response.json()
        return json_response['audio_wav_path']
    except Exception as e:
        console_msg('Ошибка получения озвучки из TTS', 'red')
        print(e)
        return None

async def generate_story():
    global generating
    console_msg('Статус генерации сценария: ' + str(generating), 'yellow')

    if generating:
        return

    try:
        generating = True
        get_voice_error = False

        headers = {
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://{API_DOMAIN}/get-item.php", headers=headers) as response:
                api_response = await response.json()

        if API_DEBUG:
            console_msg("/get-item.php:", 'cyan')
            print(api_response)

        if api_response['status'] == False:
            generating = False
            return

        console_msg('Очищаем временные файлы...')

        if api_response['type'] == 'topic':
            console_msg('Тема для ChatGPT:', 'green')
            print(api_response['topic'])

            dialogue_prompt = (
                f"Создай комедийную беседу между Владимиром Жириновским и Дмитрием Гордоном не более минуты и не более 15 реплик."
                f"Текст нужно отформатировать как \"Имя Фамилия\": \"Реплика\". Тема: {api_response['topic']}. "
            )

            data = {"topic": dialogue_prompt}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://{API_DOMAIN}/openai.php", headers=headers, json=data) as response:
                    json_response = await response.json()

            if API_DEBUG:
                console_msg("/openai.php:", 'cyan')
                print(json_response)

            messages = process_text(json_response['choices'][0]['message']['content'])
            uid_array = []

            for i, message in enumerate(messages):
                sound_url = await request_voice(message)
                if sound_url is not None:
                    uid_array.append(sound_url)
                else:
                    get_voice_error = True
                if i < len(messages) - 1:
                    await wait(2000)

            scenarios = []
            for i, message in enumerate(messages):
                scenarios.append({
                    'character': message['character'],
                    'text': message['dialogue'],
                    'sound': uid_array[i]
                })

            if not get_voice_error:
                data = {
                    'requestor_id': api_response['requestor_id'],
                    'type': 'topic',
                    'characters': 1,
                    'source': api_response['source'],
                    'user_id': api_response['user_id'],
                    'topic': api_response['topic'],
                    'topic_original': api_response['topic_original'],
                    'priority': api_response['priority'],
                    'scenario': scenarios
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(f"https://{API_DOMAIN}/push-item.php", headers=headers, json=data) as response:
                        json_response = await response.json()
                
                if API_DEBUG:
                    console_msg("/push-item.php:", 'cyan')
                    print(json_response)
            else:
                console_msg('В массиве озвучек присутствует ошибка - пропускаем сценарий', 'red')
        generating = False

    except Exception as e:
        generating = False
        console_msg('Ошибка генерации сценария:', 'red')
        print(e)

app = web.Application()

async def handle_ping(request):
    return web.Response(text='Pong!')

async def handle_get_scenario(request):
    console_msg('getScenario', 'yellow')
    try:
        headers = {
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://{API_DOMAIN}/load.php", headers=headers) as response:
                api_response = await response.json()

        if API_DEBUG:
            console_msg("/load.php:", 'cyan')
            print(api_response)

        if api_response['status']:
            if isinstance(api_response.get('characters'), str):
                try:
                    api_response['characters'] = json.loads(api_response['characters'])
                except Exception as e:
                    console_msg('Ошибка парсинга apiResponse.characters', 'red')
                    print(e)
                    api_response['characters'] = []

            if isinstance(api_response.get('scenario'), str):
                try:
                    api_response['scenario'] = json.loads(api_response['scenario'])
                except Exception as e:
                    console_msg('Ошибка парсинга apiResponse.scenario', 'red')
                    print(e)
                    api_response['scenario'] = []

            return web.json_response(api_response)
        else:
            return web.json_response({'status': "No Scenarios Available"}, status=204)
    except Exception as e:
        console_msg('Ошибка получения сценария с помощью запроса getScenario', 'red')
        print(e)
        return web.json_response({'status': "Failed", 'message': str(e)}, status=500)

async def handle_check_scenario(request):
    console_msg('checkScenario', 'yellow')
    try:
        headers = {
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://{API_DOMAIN}/skip.php", headers=headers) as response:
                api_response = await response.json()

        if API_DEBUG:
            console_msg("/skip.php:", 'cyan')
            print(api_response)

        counter_value = api_response['counter']
        console_msg(f'Кол-во /skip: {counter_value}', 'yellow')

        if counter_value > 5:
            return web.json_response({'skip': True})
        else:
            return web.json_response({'skip': False})

    except Exception as e:
        console_msg('Ошибка проверки таблицы skip: ', 'red')
        print(e)
        return web.json_response({'skip': False})


app.add_routes([
    web.get('/ping', handle_ping),
    web.get('/story/getScenario', handle_get_scenario),
    web.get('/story/checkScenario', handle_check_scenario)
])

def setup_cors(app):
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)
setup_cors(app)

async def run_web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 3001)
    await site.start()
    console_msg("LATE NIGHT AI is listening on port 3001", 'green')
    while True:
        await asyncio.sleep(3600)

async def generate_story_loop():
    while True:
        await generate_story()
        await asyncio.sleep(5)

async def main():
    asyncio.create_task(generate_story_loop())
    await run_web_server()

if __name__ == "__main__":
    asyncio.run(main())