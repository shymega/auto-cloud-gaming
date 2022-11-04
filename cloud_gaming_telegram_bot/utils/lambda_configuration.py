from os import getenv
from typing import Optional


class LambdaConfiguration:
    def __init__(self):
        # This class doesn't initialise anything, but instead dynamically gets
        # relevant environmental variables from the Lambda function's run-time
        # envronment.
        pass

    @staticmethod
    def get_telegram_token() -> Optional[str]:
        try:
            return getenv("LAMBDA_FUNC_TELEGRAM_TOKEN")
        except KeyError:
            # Return None, as we can't get the env var
            return None

    @staticmethod
    def get_aws_access_tokens() -> dict[str, Optional[str]]:
        response_dict = {}

        try:
            response_dict["aws_access_key_id"] = getenv("LAMBDA_FUNC_AWS_ACCESS_KEY_ID")
        except KeyError:
            # Set value of key to None, as we can't get the env var
            response_dict["aws_access_key_id"] = None

        try:
            response_dict["aws_secret_access_key"] = getenv(
                "LAMBDA_FUNC_AWS_SECRET_ACCESS_KEY"
            )
        except KeyError:
            # in future, return graceful errror
            # Set value of key to None, as we can't get the env var
            response_dict["aws_secret_access_key"] = None

        return response_dict

    @staticmethod
    def get_telegram_owner_id() -> Optional[str]:
        try:
            return getenv("LAMBDA_FUNC_TELEGRAM_OWNER_ID")
        except KeyError:
            # Return None, as we can't get the env var
            return None
