from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse, Response

from photos_api.services.photos import PhotosService

router = APIRouter(prefix='/api', tags=['Photos'])


@router.get(
    '/{photo_id}',
    responses={
        404: {
            'response_model': None
        }
    }
)
async def get_photo(
        photo_id: str,
        photo_service: PhotosService = Depends()
):
    return StreamingResponse(
        await photo_service.get_photo(photo_id),
        media_type="image/jpg")


@router.post('/{photo_id}')
async def save_photo(
        photo_id: str,
        photo: UploadFile,
        photo_service: PhotosService = Depends()
):
    await photo_service.save_photo(photo_id, photo)
    return {"success": True}


@router.delete('/{photo_id}')
async def delete_photo(
        photo_id: str,
        photo_service: PhotosService = Depends()
):
    await photo_service.delete_photo(photo_id)
    return {"success": True}
