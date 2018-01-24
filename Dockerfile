FROM python:3.6.3

RUN mkdir -p /code
WORKDIR /code

ADD ./requirements.txt .

RUN pip install -r requirements.txt

ADD ./ ./

EXPOSE 9999

CMD PYTHONPATH=./:$PYTHONPATH python zhchecker/server.py
