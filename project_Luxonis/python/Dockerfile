FROM python:3.9

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/app/src

COPY scrape.py ./