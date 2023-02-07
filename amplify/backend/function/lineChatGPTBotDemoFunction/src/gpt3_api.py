import requests
import const

GPT3_COMPLETIONS_ENDPOINT = 'https://api.openai.com/v1/completions'
GPT3_MODEL = 'text-davinci-003'
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {const.OPEN_AI_API_KEY}'
}
MAX_TOKENS = 1000
TEMPERATURE = 0.5


def completions(prompt):

    completions_data = {
        'prompt': prompt,
        'model': GPT3_MODEL,
        'max_tokens': MAX_TOKENS,
        'n': 1,
        'stop': None,
        'temperature': TEMPERATURE
    }

    try:
        response = requests.post(GPT3_COMPLETIONS_ENDPOINT, headers=HEADERS, json=completions_data)
        response_json = response.json()
        return response_json['choices'][0]['text']
    except Exception as e:
        raise e
