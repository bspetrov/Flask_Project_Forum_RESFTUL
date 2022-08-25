import boto3
from botocore.exceptions import ClientError

from decouple import config
from werkzeug.exceptions import InternalServerError


class SimpleEmailService:
    def __init__(self):
        self.subject_data = "Thank you for registering!"
        self.email_data = "Thank you for joining Forumy, we are glad that you decided to participate and help other " \
                          "members of our community "
        self.region_name = config("AWS_SES_REGION")
        self.access = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET")
        self.client = boto3.client("ses", region_name=self.region_name, aws_access_key_id=self.access,
                                   aws_secret_access_key=self.secret)
        self.charset = "UTF-8"

    def send_mail(self, destination_email):
        try:
            response = self.client.send_email(
                Destination={
                    "ToAddresses": [
                        destination_email,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": self.charset,
                            "Data": self.email_data,
                        }
                    },
                    "Subject": {
                        "Charset": self.charset,
                        "Data": self.subject_data,
                    },
                },
                Source="pothednb@gmail.com",
            )
            return response
        except ClientError as ex:
            raise InternalServerError("SES is not available at the moment")
