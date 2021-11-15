FROM python:3.8.2-alpine

RUN apk --no-cache add curl
WORKDIR /service
COPY /service /service
EXPOSE 5004

RUN pip3 install -r requirements.txt


ENTRYPOINT python service.py
