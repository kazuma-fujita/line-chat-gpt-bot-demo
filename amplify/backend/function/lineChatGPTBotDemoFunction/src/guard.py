import logging
import hashlib
import hmac
import base64
import const


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def verify_request(event):
    # リクエストの検証
    x_line_signature = event["headers"]["x-line-signature"] if event["headers"]["x-line-signature"] else event["headers"]["X-Line-Signature"]
    body = event["body"]
    hash = hmac.new(const.LINE_CHANNEL_SECRET.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if signature != x_line_signature.encode():
        logger.error('verify error')
        raise Exception
