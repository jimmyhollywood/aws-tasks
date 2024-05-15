from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import json

_LOG = get_logger('HelloWorld-handler')


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        print(event)
        print(context)
        context = event.get("requestContext", {})
        http_dict = context.get("http", {})
        path = http_dict.get("path", "") if http_dict else ""
        method = http_dict.get("method", "") if http_dict else ""
        # response = {
        #     "statusCode": 200,
        #     "body": {
        #         "statusCode": 200,
        #     }}
        if path == "/hello":
            # response["body"]["message"] = "Hello from Lambda"
            # print("Returning: ", response)
            return json.dumps({
                'statusCode': 200,
                'message': 'Hello from Lambda'
            })
        else:
            return json.dumps({
                'statusCode': 400,
                'message': f'Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}'
            })


HANDLER = HelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
