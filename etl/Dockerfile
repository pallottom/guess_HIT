FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN pip3 install --upgrade pip
WORKDIR /etl

COPY ./requirements.txt /etl/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /etl

CMD python3 etl.py