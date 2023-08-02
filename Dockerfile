FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY setup.py ./
COPY ./photos_api ./photos_api
RUN pip3 install .

CMD init_db && \
    cd photos_api && \
    alembic -c ./alembic.prod.ini upgrade head && \
    cd /app && \
    gunicorn photos_api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80
