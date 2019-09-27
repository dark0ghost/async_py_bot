FROM Debian:10
FROM python:3.7.4

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ADD . /usr/src/app

RUN  apt-get install python3-distutils
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gino

COPY . .

RUN sh -ac 'cd /usr/src/app && python3 start_poling.py'
RUN sh -ac 'cd /usr/src/app./model/auth/ && python3 Auth.py'



RUN echo "run"