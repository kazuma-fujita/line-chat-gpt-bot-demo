import logging
import boto3
from botocore.exceptions import ClientError

AWS_REGION = "ap-northeast-1"

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
