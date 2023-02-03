import logging
import requests
import const

GPT3_COMPLETIONS_ENDPOINT = 'https://api.openai.com/v1/completions'
GPT3_MODEL = 'text-davinci-003'
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {const.OPEN_AI_API_KEY}'
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def completions(prompt):
    completions_data = {
        'prompt': prompt,
        'model': GPT3_MODEL,
        'max_tokens': 1000,
        'n': 1,
        'stop': None,
        'temperature': 0.5
    }
    response = requests.post(GPT3_COMPLETIONS_ENDPOINT, headers=HEADERS, json=completions_data)
    response_json = response.json()
    return response_json['choices'][0]['text']
