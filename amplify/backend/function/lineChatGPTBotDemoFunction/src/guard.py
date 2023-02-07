import hashlib
import hmac
import base64
import const
import app_logger

logger = app_logger.init()


def verify_request(event):
    # リクエストの検証
    x_line_signature = event["headers"]["x-line-signature"] if event["headers"]["x-line-signature"] else event["headers"]["X-Line-Signature"]
    body = event["body"]
    hash = hmac.new(const.LINE_CHANNEL_SECRET.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if signature != x_line_signature.encode():
        raise Exception("Request verification failed. Request came from a non-LINE server source.")
