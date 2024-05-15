from tests.test_hello_world import HelloWorldLambdaTestCase


class TestSuccess(HelloWorldLambdaTestCase):

    def test_success(self):
        request_data = {'version': '2.0', 'routeKey': '$default', 'rawPath': '/hello', 'rawQueryString': '',
                        'headers': {'x-amzn-tls-cipher-suite': 'TLS_AES_128_GCM_SHA256',
                                    'x-amzn-tls-version': 'TLSv1.3',
                                    'x-amzn-trace-id': 'Root=1-6644b7d9-44482fab4f1e97ba29764a41',
                                    'x-forwarded-proto': 'https',
                                    'host': 'trqljtkytg4vm5lzkdy5iubzjy0qgimy.lambda-url.eu-central-1.on.aws',
                                    'x-forwarded-port': '443', 'x-forwarded-for': '3.66.167.221',
                                    'accept-encoding': 'gzip, deflate', 'accept': '*/*',
                                    'user-agent': 'python-requests/2.31.0'},
                        'requestContext': {'accountId': 'anonymous', 'apiId': 'trqljtkytg4vm5lzkdy5iubzjy0qgimy',
                                           'domainName': 'trqljtkytg4vm5lzkdy5iubzjy0qgimy.lambda-url.eu-central-1.on.aws',
                                           'domainPrefix': 'trqljtkytg4vm5lzkdy5iubzjy0qgimy',
                                           'http': {'method': 'GET', 'path': '/hello', 'protocol': 'HTTP/1.1',
                                                    'sourceIp': '3.66.167.221', 'userAgent': 'python-requests/2.31.0'},
                                           'requestId': '44fde757-029e-45a9-ae33-95373edde4cf', 'routeKey': '$default',
                                           'stage': '$default', 'time': '15/May/2024:13:25:45 +0000',
                                           'timeEpoch': 1715779545482}, 'isBase64Encoded': False}
        self.assertEqual(self.HANDLER.handle_request(request_data, dict())["body"], {"statusCode": 200,
                                                                                     "message": "Hello from Lambda"})
