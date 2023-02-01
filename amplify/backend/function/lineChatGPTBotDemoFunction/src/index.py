import json
import logging
import requests
import boto3
from botocore.exceptions import ClientError
from linebot import LineBotApi
from linebot.models import TextSendMessage

AWS_REGION = "ap-northeast-1"
# LINE
REQUEST_URL = 'https://api.line.me/v2/bot/message/reply'
REQUEST_METHOD = 'POST'
# OPEN_AI
OPEN_AI_MODEL = 'text-davinci-003'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret(secret_key):
    try:
        ssm = boto3.client('ssm', region_name=AWS_REGION)
        response = ssm.get_parameter(
            Name=secret_key,
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except ClientError as e:
        logger.error(e)
        raise
    # except ClientError as e:
    #     if e.response['Error']['Code'] == 'DecryptionFailureException':
    #         raise e
    #     elif e.response['Error']['Code'] == 'InternalServiceErrorException':
    #         raise e
    #     elif e.response['Error']['Code'] == 'InvalidParameterException':
    #         raise e
    #     elif e.response['Error']['Code'] == 'InvalidRequestException':
    #         raise e
    #     elif e.response['Error']['Code'] == 'ResourceNotFoundException':
    #         raise e


def completions(prompt, model, api_key):
    completions_url = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    completions_data = {
        'prompt': prompt,
        'model': model,
        'max_tokens': 100,
        'n': 1,
        'stop': None,
        'temperature': 0.5
    }
    response = requests.post(completions_url, headers=headers, json=completions_data)
    response_json = response.json()
    return response_json['choices'][0]['text']


def handler(event, context):
    logger.info(event)

    # open_ai_api_key = get_secret('OPEN_AI_API_KEY')
    # line_channel_access_token = get_secret('LINE_CHANNEL_ACCESS_TOKEN')
		# TODO: /amplify/d2uom1q8k1be5p/dev/AMPLIFY_lineChatGPTBotDemoFunction_ までを環境変数に切り出す
    open_ai_api_key = get_secret('/amplify/d2uom1q8k1be5p/dev/AMPLIFY_lineChatGPTBotDemoFunction_OPEN_AI_API_KEY')
    line_channel_access_token = get_secret('/amplify/d2uom1q8k1be5p/dev/AMPLIFY_lineChatGPTBotDemoFunction_LINE_CHANNEL_ACCESS_TOKEN')
    event_body = json.loads(event['body'])
    print(event_body)
    try:
        # LINEからメッセージを受信
        if event_body['events'][0]['type'] == 'message' and event_body['events'][0]['message']['type'] == 'text':
            # リプライ用トークン
            replyToken = event_body['events'][0]['replyToken']
            # 受信メッセージ
            prompt = event_body['events'][0]['message']['text']
            print(replyToken)
            print(prompt)
            # GPT-3
            completed_text = completions(prompt, OPEN_AI_MODEL, open_ai_api_key)
            print(completed_text)
            # チャネルアクセストークンを使用して、LineBotApiのインスタンスを作成
            line_bot_api = LineBotApi(line_channel_access_token)
            # メッセージを返信
            line_bot_api.reply_message(replyToken, TextSendMessage(text=completed_text))

    # エラーが起きた場合
    except Exception as e:
        print('Error')
        print(e)
        # LINE Developers記載によるとエラーが発生した際も200を返却
        # https://developers.line.biz/ja/reference/messaging-api/#response
        # return {'statusCode': 500, 'body': json.dumps('Exception occurred.')}
        return {'statusCode': 200, 'body': json.dumps('Exception occurred.')}

    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}