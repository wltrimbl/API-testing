# MG-RAST API-testing

FROM alpine:3.7

RUN apk update && apk add make bash curl python pytest file py-pip
RUN pip install pytest-json

COPY . /root/

WORKDIR /root

