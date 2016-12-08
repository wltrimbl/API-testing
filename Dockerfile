# MG-RAST API-testing

FROM alpine:3.4

RUN apk update && apk add curl python

#FROM ubuntu 14.04
#RUN apt-get update && apt-get install -y \
#  python \
#  curl 

COPY . /root/

WORKDIR /root

#CMD ["/root/API-testing.py", "--fast", "-w /root/test", "-b /root/data", "--jsonfile /tmp_host/api_test.json"]

