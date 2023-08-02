from fastapi import FastAPI
from pydantic_settings import BaseSettings

from photos_api import api as api_module
from photos_api.services import base as services_base_module
from photos_api.services import s3 as s3_service_module


class Config(BaseSettings):
    backend_token: str = '123456'
    photos_path: str = './images'
    aws_access_key_id: str = ''
    aws_secret_access_key: str = ''
    aws_bucket: str = 'test'


def init_web_application(config=Config()):
    api_module.backend_token = config.backend_token
    services_base_module.BaseService.photos_path = config.photos_path
    s3_service_module.S3Service.aws_access_key_id = config.aws_access_key_id
    s3_service_module.S3Service.aws_secret_access_key = config.aws_secret_access_key
    s3_service_module.S3Service.bucket = config.aws_bucket

    application = FastAPI(
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )

    from photos_api.api.hello import router as hello_router
    from photos_api.api.photo import router as photo_router

    application.include_router(hello_router)
    application.include_router(photo_router)

    return application


def run() -> FastAPI:
    application = init_web_application()
    return application


app = run()
