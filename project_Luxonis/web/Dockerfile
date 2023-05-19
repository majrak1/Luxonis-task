FROM http.server:latest

FROM python:latest

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py /
EXPOSE 8080
CMD python -m http.server 8080