FROM python:3.11.2-slim-buster

RUN mkdir /app
RUN mkdir /app/data
RUN mkdir /app/logs
WORKDIR /app
ADD requirements.txt .
ADD ./app .
RUN apt-get update && \
    apt-get upgrade -y && \
    pip install -U pip && \
    pip install -r requirements.txt && \
    apt-get autoclean


EXPOSE 8009

ENTRYPOINT ["python"]
CMD ["main.py"]