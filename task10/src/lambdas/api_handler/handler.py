import os

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import json
import re
import boto3
import os

_LOG = get_logger('ApiHandler-handler')


def get_user_pool_id(client, user_pool_name: str) -> str:
    user_pools = client.list_user_pools(MaxResults=60)
    for user_pool in user_pools["UserPools"]:
        # _LOG.info(f"User pool: {user_pool}")
        if user_pool["Name"] == user_pool_name:
            return user_pool["Id"]


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def signup(self, data: dict):

        client = boto3.client('cognito-idp')
        user_pool_name = os.environ.get("USER_POOL")
        _LOG.info(f"Looking for user pool id for: {user_pool_name}")

        user_pool_id = get_user_pool_id(client, user_pool_name)
        _LOG.info(f"User pool id: {user_pool_id}")

        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        email = data.get("email", "")
        password = data.get("password", "")

        try:

            email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_pattern, email):
                _LOG.error('Invalid email')
                raise Exception('Invalid email')

            pass_pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^\w\s]).{12,}$'
            if not re.match(pass_pattern, password):
                _LOG.info('Invalid password')
                raise Exception('Invalid password')

            resp = client.admin_create_user(
                UserPoolId=user_pool_id,
                Username=email,
                UserAttributes=[
                    {
                        "Name": "email",
                        "Value": email
                    },
                    {
                        "Name": "name",
                        "Value": first_name
                    },
                    {
                        "Name": "family_name",
                        "Value": last_name
                    }
                ],
                TemporaryPassword=password
            )
            _LOG.info(f"User create response: {resp}")
        except Exception as e:
            _LOG.error(f"Exception during create user: {e}")
            raise

        try:
            resp = client.admin_set_user_password(
                UserPoolId=user_pool_id,
                Username=email,
                Password=password,
                Permanent=True
            )
            _LOG.info(f'set_user_password permanent response: {resp}')
        except Exception:
            raise

        return {
            "statusCode": 200
        }

    def signin(self, data: dict):

        email = data.get("email", "")
        password = data.get("password", "")

        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            _LOG.error('Invalid email')
            raise Exception('Invalid email')

        pass_pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^\w\s]).{12,}$'
        if not re.match(pass_pattern, password):
            _LOG.info('Invalid password')
            raise Exception('Invalid password')

        client = boto3.client('cognito-idp')
        user_pool_name = os.environ.get("USER_POOL")
        _LOG.info(f"Looking for user pool id for: {user_pool_name}")

        user_pool_id = get_user_pool_id(client, user_pool_name)
        _LOG.info(f"User pool id: {user_pool_id}")

        response = client.list_user_pool_clients(
            UserPoolId=user_pool_id,
            MaxResults=10
        )

        client_app = 'client'
        for app_client in response['UserPoolClients']:
            if app_client['ClientName'] == client_app:
                app_client_id = app_client['ClientId']

        response = client.initiate_auth(
            ClientId=app_client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )

        # access_token = response['AuthenticationResult']['AccessToken']
        token = response['AuthenticationResult']['IdToken']

        return {
            'statusCode': 200,
            'body': json.dumps({'accessToken': token})
        }



    def tables(self):
        ...


    def reservations(self):
        ...


    def handle_request(self, event, context):
        """
        Explain incoming event here
        """

        path = event.get("path", None)
        method = event.get("methodHttp", "")
        _LOG.info(f"Event: {event}")
        _LOG.info(f"Context: {context}")
        body = json.loads(event['body'])
        try:
            if path:
                if path == "/signup":
                    return self.signup(body)
                elif path == "/signin":
                    return self.signin(body)
                elif path == "/tables":
                    if method == "GET":
                        pass
                    elif method == "POST":
                        pass
                elif path == "reservations":
                    if method == "GET":
                        pass
                    elif method == "POST":
                        pass
        except Exception:
            return {
                "statusCode": 400
            }


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
