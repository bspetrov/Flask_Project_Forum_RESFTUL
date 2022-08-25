import boto3
from botocore.exceptions import ClientError
from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET")
        self.region = config("AWS_REGION")
        self.bucket = config("AWS_BUCKET")

        self.s3 = boto3.client("s3", region_name=self.region, aws_access_key_id=self.key,
                               aws_secret_access_key=self.secret)

    def upload_attachment(self, path, key):
        try:
            self.s3.upload_file(path, self.bucket, key)
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        except ClientError as ex:
            raise InternalServerError("S3 is not available at the moment")

    def remove_attachment(self, key):
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
            return "Object deleted!"
        except ClientError as ex:
            raise InternalServerError("S3 is not available at the moment!")
