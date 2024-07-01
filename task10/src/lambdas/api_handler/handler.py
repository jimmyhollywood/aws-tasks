from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """

        path = event.get("path", None)
        method = event.get("methodHttp", "")
        if path:
            if path == "/signup":
                ...
            elif path == "/signin":
                ...
            elif path == "/tables":
                if method == "GET":
                    ...
                elif method == "POST":
                    ...
            elif path == "reservations":
                if method == "GET":
                    ...
                elif method == "POST":
                    ...

        return 200


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
