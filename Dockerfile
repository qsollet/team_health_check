FROM python:3.6-alpine

RUN apk add build-base
RUN mkdir /src
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
RUN pip install gunicorn

ENTRYPOINT ["./run.sh"]
