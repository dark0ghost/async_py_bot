FROM python:3.7.4

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ADD . /usr/src/app

RUN  apt-get install python3-distutils
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


RUN echo "run"