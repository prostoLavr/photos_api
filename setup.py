from setuptools import setup, find_packages


install_requires = [
    'asyncpg',
    'pydantic',
    'fastapi',
    'uvicorn',
    'sqlalchemy[asyncio]',
    'gunicorn',
    'loguru'
]

setup(
    name='photos-api',
    version="0.0.1.dev1",
    description='Patient API',
    platforms=['POSIX'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'init_models = photos_api.db.base:run_init_models',
            'init_db = photos_api.db.create:run_init_db',
            'archive-all = photos_api.services.photos:PhotosService.archive_all'
        ]
    }
)

