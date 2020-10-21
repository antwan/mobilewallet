FROM alpine
FROM python:3.7

ENV PATH /usr/local/bin:$PATH

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY . /app
WORKDIR /app

COPY ./docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
