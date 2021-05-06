FROM python:3.8-slim

ADD requirements.txt /code/
RUN pip3 install -r /code/requirements.txt

ADD . /code
WORKDIR /code
CMD gunicorn -c gunicorn.conf.py cmdboss:app