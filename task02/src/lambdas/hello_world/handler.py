from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('HelloWorld-handler')


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        # print(event["requestContext"]["http"]["path"])
        context = event.get("requestContext", {})
        http_dict = context.get("http", {})
        path = http_dict.get("path", "") if http_dict else ""
        method = http_dict.get("method", "") if http_dict else ""

        if path == "/hello":
            return {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }
        return {
            "statusCode": 400,
            "message": f"Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
        }


HANDLER = HelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)


{'version': '2.0', 'routeKey': '$default', 'rawPath': '/hello', 'rawQueryString': '',
 'headers': {'x-amzn-tls-cipher-suite': 'TLS_AES_128_GCM_SHA256', 'x-amzn-tls-version': 'TLSv1.3',
             'x-amzn-trace-id': 'Root=1-6644b7d9-44482fab4f1e97ba29764a41', 'x-forwarded-proto': 'https',
             'host': 'trqljtkytg4vm5lzkdy5iubzjy0qgimy.lambda-url.eu-central-1.on.aws', 'x-forwarded-port': '443',
             'x-forwarded-for': '3.66.167.221', 'accept-encoding': 'gzip, deflate', 'accept': '*/*',
             'user-agent': 'python-requests/2.31.0'},
 'requestContext': {'accountId': 'anonymous', 'apiId': 'trqljtkytg4vm5lzkdy5iubzjy0qgimy',
                    'domainName': 'trqljtkytg4vm5lzkdy5iubzjy0qgimy.lambda-url.eu-central-1.on.aws',
                    'domainPrefix': 'trqljtkytg4vm5lzkdy5iubzjy0qgimy',
                    'http': {'method': 'GET', 'path': '/hello', 'protocol': 'HTTP/1.1', 'sourceIp': '3.66.167.221',
                             'userAgent': 'python-requests/2.31.0'},
                    'requestId': '44fde757-029e-45a9-ae33-95373edde4cf', 'routeKey': '$default', 'stage': '$default',
                    'time': '15/May/2024:13:25:45 +0000', 'timeEpoch': 1715779545482}, 'isBase64Encoded': False}
