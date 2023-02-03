import json
import logging
import guard
import line_api

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)

    try:
        guard.verify_request(event)
        line_api.reply_message(event)
    # エラーが起きた場合
    except Exception as e:
        print('Error')
        print(e)
        # LINE Developers記載によるとエラーが発生した際も200を返却
        # https://developers.line.biz/ja/reference/messaging-api/#response
        # return {'statusCode': 500, 'body': json.dumps('Exception occurred.')}
        return {'statusCode': 200, 'body': json.dumps('Exception occurred.')}

    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}
