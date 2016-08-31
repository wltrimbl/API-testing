# MG-RAST API-testing

FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
  python \
  curl 

COPY . /root/

# RUN /root/API-testing.py -f -w /root/test -b /root/data

