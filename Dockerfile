FROM alpine:3.16.2

RUN mkdir /app
COPY . /app

RUN apk update

# Install required packages
RUN apk add python3 py3-pip pcre supervisor

# Add extra packages required to install uwsgi
RUN apk add python3-dev build-base linux-headers pcre-dev


RUN pip install -r /app/requirements.txt

# Remove unsused packages
RUN apk del python3-dev build-base linux-headers pcre-dev

COPY supervisord.ini /etc/supervisor.d/supervisord.ini

EXPOSE 5000

WORKDIR /app

CMD ["/usr/bin/supervisord" ]
