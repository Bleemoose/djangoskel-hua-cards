# Docker file for building the required system starting from Ubuntu 20.04 image
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get update && apt-get install -y curl apt-utils apt-transport-https debconf-utils \
    gcc build-essential libsasl2-dev python-dev libldap2-dev libssl-dev ldap-utils python3-pip \
    netcat net-tools gettext
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /reqs/
RUN pip3 install -r /reqs/requirements.txt
COPY ./django_init.sh /run
RUN chmod +x /run/django_init.sh
COPY ./code /code
CMD  sh /run/django_init.sh
