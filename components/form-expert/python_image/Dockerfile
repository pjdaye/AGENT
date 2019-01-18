FROM python:3.7.1-alpine3.8

RUN apk add build-base gcc abuild binutils binutils-doc gcc-doc

COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

RUN python -m spacy download en