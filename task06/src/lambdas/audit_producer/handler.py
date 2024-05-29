import datetime

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import os
import boto3
import uuid

_LOG = get_logger('AuditProducer-handler')


class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info(event)

        conf_table_name = os.environ.get("CONFIGURATION_TABLE")
        audit_table_name = os.environ.get("AUDIT_TABLE")
        _LOG.info(f"Configuration table: {conf_table_name}")
        _LOG.info(f"Audit table: {audit_table_name}")

        db = boto3.resource("dynamodb")

        audit_t = db.Table(audit_table_name)
        now = datetime.datetime.now().isoformat()
        try:
            ev = event["Records"][0]
            ev_name = ev["eventName"]
            if ev_name == "INSERT":
                obj = {
                    "id": str(uuid.uuid4()),
                    "itemKey": ev['dynamodb']['Keys']['key']['S'],
                    "modificationTime": now,
                    "newValue": {
                        "key": ev['dynamodb']['NewImage']['key']['S'],
                        "value": int(ev['dynamodb']['NewImage']['value']['N'])
                    }
                }
            elif ev_name == "MODIFY":
                obj = {
                    "id": str(uuid.uuid4()),
                    "itemKey": ev['dynamodb']['Keys']['key']['S'],
                    "modificationTime": now,
                    "updatedAttribute": "value",
                    "oldValue": int(ev['dynamodb']['OldImage']['value']['N']),
                    "newValue": int(ev['dynamodb']['NewImage']['value']['N'])
                }
            audit_t.put_item(Item=obj)

        except Exception as e:
            _LOG.error(e)
        return 200
    

HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
