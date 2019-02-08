# MG-RAST API-testing

# docker build -t mgrast/api-testing .

FROM debian:stretch

RUN apt-get update && apt-get install -y make curl python python-pip

RUN pip install --upgrade pip

RUN pip install pytest pytest-json

COPY . /root/

WORKDIR /root
