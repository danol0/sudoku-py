FROM python:3.11.5

RUN mkdir app

# Cannot clone private gitlab repo without setting up access key as a secret
# For simplicity, will copy files locally instead

COPY requirements.txt app
COPY src app/src
COPY test app/test

WORKDIR /app
RUN pip install -r requirements.txt
