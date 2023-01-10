FROM ubuntu:20.04

# Add ONL user
ARG USER=onl

WORKDIR /home/${USER}

ARG DEBIAN_FRONTEND=noninteractive
# Install dependency
RUN apt-get update && apt-get install -y \
    python3-pip wget unzip gocr imagemagick iperf3

RUN pip3 install pytest numpy requests soundfile paramiko scp

COPY bwmur bwmur
