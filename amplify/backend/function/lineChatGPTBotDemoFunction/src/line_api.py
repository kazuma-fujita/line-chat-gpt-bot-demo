import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
import const
import gpt3_api
import app_logger

logger = app_logger.init()


def reply_message(event):
    try:
        event_body = json.loads(event['body'])
        # LINEからメッセージを受信
        if event_body['events'][0]['type'] == 'message' and event_body['events'][0]['message']['type'] == 'text':
            # リプライ用トークン
            replyToken = event_body['events'][0]['replyToken']
            # 受信メッセージ
            prompt = event_body['events'][0]['message']['text']
            # GPT-3
            completed_text = gpt3_api.completions(prompt)
            response_message = completed_text.strip()
            # チャネルアクセストークンを使用して、LineBotApiのインスタンスを作成
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
            # メッセージを返信
            line_bot_api.reply_message(replyToken, TextSendMessage(text=response_message))
            # log
            logger.info(prompt)
            logger.info(response_message)

    except Exception as e:
        raise e
