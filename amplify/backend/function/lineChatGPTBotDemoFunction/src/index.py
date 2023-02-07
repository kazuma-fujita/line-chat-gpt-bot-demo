import json
import guard
import line_api
import app_logger

logger = app_logger.init()


def handler(event, context):
    logger.info(event)

    try:
        guard.verify_request(event)
        line_api.reply_message(event)
    except Exception as e:
        logger.error(e)
        # エラーが発生した際も200を返却
        # https://developers.line.biz/ja/reference/messaging-api/#response
        return {'statusCode': 200, 'body': json.dumps(f'Exception occurred: {e}')}

    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}
