FROM python:3-alpine

COPY ./src/contest_calculate_commenters/requirements.txt /requirements.txt

RUN apk add --no-cache binutils && pip install -r /requirements.txt