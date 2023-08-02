from photos_api.services.base import BaseService
from photos_api import api as api_module
from photos_api.services.s3 import S3Service

from loguru import logger
from fastapi import HTTPException, status, Header, Depends
from PIL import Image

import os
import string
from inspect import iscoroutine


class PhotosService(BaseService):
    available_symbols = string.ascii_letters + string.digits

    def __init__(
            self, token=Header(),
            s3_service: S3Service = Depends(S3Service)
    ):
        self.s3_service = s3_service
        if token != api_module.backend_token:
            logger.info(f"Ban user with {token=}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def _get_path(cls, photo_id: str, directory: str = '') -> str:
        if '.' in photo_id:
            raise HTTPException(status_code=status.HTTP_423_LOCKED)
        path = os.path.join(cls._get_directory(directory), photo_id + '.jpeg')
        return path

    @classmethod
    def _get_directory(cls, directory: str = ""):
        path = os.path.join(cls.photos_path, directory)
        if '.' in directory:
            raise HTTPException(status_code=status.HTTP_423_LOCKED)
        return path

    @classmethod
    async def _get_photo_by_path(
            cls,
            path: str
    ):
        try:
            with open(path, mode="rb") as file:
                yield file.read()
        except FileNotFoundError:
            logger.warning('No found file {path}', path=path)
            with open(os.path.join(cls.photos_path, 'nophoto.png'), mode="rb") as file:
                yield file.read()

    async def get_photo(
            self, photo_id: str
    ):
        # path = self._get_path(photo_id, directory)
        # yield await anext(self._get_photo_by_path(path))
        return self.s3_service.stream(photo_id)

    async def save_photo(
            self,
            photo_id: str,
            upload_photo=None,
    ):
        if upload_photo is None:
            raise AttributeError('Set upload_photo')
        read_data = upload_photo.read()
        if iscoroutine(read_data):
            awaited_data = await read_data
            read_data = awaited_data
        # image = Image.open(read_data)
        # image.save(cls._get_path(photo_id, directory))
        await self.s3_service.put(photo_id, read_data)

    async def delete_photo(
            self,
            photo_id: str
    ):
        await self.s3_service.delete(photo_id)

    @staticmethod
    def archive_all():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--path', type=str)

        walk_path = parser.parse_args().path
        PhotosService.photos_path = walk_path

        for root, _, files in os.walk(PhotosService.photos_path):
            for file_name in files:
                print(root, file_name)
                with open(os.path.join(root, file_name), 'rb') as file:
                    PhotosService.save_photo(file_name, file, root[len(walk_path):])

