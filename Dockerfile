# # Use the official Alpine Linux image as the base
# FROM ubuntu:latest


# RUN apt update

# WORKDIR /app

# # systemctl start docker
# # !dockerd --iptables=false

# COPY . /app

# RUN pip install -r requirements.txt
# # RUN !dockerd --iptables=false
# # rm rf /var/lib/docker/network

# VOLUME /app

# CMD ["/bin/bash"]

FROM docker:latest

# Install Docker Compose
RUN apk update

RUN apk --no-cache add \
    docker-compose \
    python3 \
    py3-pip \
    sudo \
    git

WORKDIR /app

COPY . /app

VOLUME /app

RUN pip install -r requirements.txt

# This entrypoint starts the Docker daemon and runs your command
ENTRYPOINT ["dockerd-entrypoint.sh"]
CMD ["/bin/sh"]
