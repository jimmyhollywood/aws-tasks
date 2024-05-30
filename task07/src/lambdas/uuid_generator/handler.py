from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import uuid
import  datetime
import boto3
import json

_LOG = get_logger('UuidGenerator-handler')


class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        now = datetime.datetime.now().isoformat()[:23] + "Z"
        res = {
            "ids": list([str(uuid.uuid4() for _ in range(10))])
        }
        s3 = boto3.client('s3')
        s3.put_object(Body=json.dumps(res), Bucket="cmtr-27efb7c4-uuid-storage-test", Key=now)


HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
