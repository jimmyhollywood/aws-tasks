from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import requests

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
        response = {
            "body": {
                "statusCode": 200,
            }}
        if path == "/hello":
            response["body"]["message"] = "Hello from Lambda"
            print("Returning: ", response)
        else:
            response["body"]["statusCode"] = 400
            response["body"][
                "message"] = f"Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
            print("Returning: ", response)
        return response


HANDLER = HelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
