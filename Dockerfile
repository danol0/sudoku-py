FROM continuumio/miniconda3

RUN mkdir app

COPY src app/src
COPY test app/test
COPY environment.yml app
COPY config.json app

WORKDIR /app
RUN conda env update -f environment.yml --name base
