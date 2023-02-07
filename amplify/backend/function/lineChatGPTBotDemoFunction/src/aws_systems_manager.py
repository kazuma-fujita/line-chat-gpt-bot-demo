import boto3
from botocore.exceptions import ClientError
import app_logger

logger = app_logger.init()

AWS_REGION = "ap-northeast-1"


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
        raise e
