import aioboto3
from loguru import logger

from photos_api.services.base import BaseService


class S3Service(BaseService):
    aws_access_key_id = ''
    aws_secret_access_key = ''
    bucket = ''

    def __init__(self):
        self.session = aioboto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

    async def put(self, key, body):
        async with self.session.client(
                service_name='s3', endpoint_url='https://s3.storage.selcloud.ru'
        ) as client:
            await client.put_object(Bucket=self.bucket, Key=key, Body=body)

    async def delete(self, key):
        async with self.session.client(
                service_name='s3', endpoint_url='https://s3.storage.selcloud.ru'
        ) as client:
            await client.delete_object(Bucket=self.bucket, Key=key)

    async def stream(self, key):
        async with self.session.client(
                service_name='s3', endpoint_url='https://s3.storage.selcloud.ru'
        ) as client:
            result_object = await client.get_object(
                Bucket=self.bucket,
                Key=key,
            )
            async for chunk in result_object['Body']:
                yield chunk
