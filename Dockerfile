FROM python:3.6.3

RUN mkdir -p /code
WORKDIR /code

ADD ./requirements.txt .

RUN pip install -r requirements.txt

ADD ./ ./

EXPOSE 9999

CMD python zhchecker/server.py
