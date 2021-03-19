FROM ubuntu:20.04

ENV POETRY_VERSION=1.1.5

COPY . /app
WORKDIR /app

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && apt-get install -y --no-install-recommends python3.8-dev python3-pip \
    && apt-get install -y --no-install-recommends openjdk-8-jdk openjdk-8-jre \
    && pip3 install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false \
    && poetry install \
    && python3 special_students/pipelines/data_pipeline.py

EXPOSE 80

CMD ["streamlit", "run", "special_students/app.py"]