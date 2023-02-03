import json
import logging
from linebot import LineBotApi
from linebot.models import TextSendMessage
import const
import gpt3_api

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def reply_message(event):
    try:
        event_body = json.loads(event['body'])
        # LINEからメッセージを受信
        if event_body['events'][0]['type'] == 'message' and event_body['events'][0]['message']['type'] == 'text':
            # リプライ用トークン
            replyToken = event_body['events'][0]['replyToken']
            # 受信メッセージ
            prompt = event_body['events'][0]['message']['text']
            print(replyToken)
            print(prompt)
            # GPT-3
            completed_text = gpt3_api.completions(prompt)
            print(completed_text)
            response_message = completed_text.strip()
            print(response_message)
            # チャネルアクセストークンを使用して、LineBotApiのインスタンスを作成
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
            # メッセージを返信
            line_bot_api.reply_message(replyToken, TextSendMessage(text=response_message))

    # エラーが起きた場合
    except Exception as e:
        raise e
