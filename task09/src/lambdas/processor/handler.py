from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import requests
import boto3
import os
import uuid

_LOG = get_logger('Processor-handler')


class Processor(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        table_name = "cmtr-27efb7c4-Weather-test"
        db = boto3.resource("dynamodb")
        table = db.Table(table_name)
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
        item = {
            'id': str(uuid.uuid4()),
            "forecast": {
            "elevation": response['elevation'],
            "generationtime_ms": response['generationtime_ms'],
            "hourly": {
                "temperature_2m": response['hourly']['temperature_2m'],
                "time": response['hourly']['time']
            },
            "hourly_units": {
                "temperature_2m": response['hourly_units']['temperature_2m'],
                "time": response['hourly_units']['time']
            },
            "latitude": response['latitude'],
            "longitude": response['longitude'],
            "timezone": response['timezone'],
            "timezone_abbreviation": response['timezone_abbreviation'],
            "utc_offset_seconds": response['utc_offset_seconds']
            }
        }
        table.put_item(Item=item)


HANDLER = Processor()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
