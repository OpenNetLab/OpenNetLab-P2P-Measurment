# OpenNetLab-P2P-Measurment
## Introduction
This is a network measurement tool that currently contains parameters for measuring network bandwidth, which is designed with containerization in mind.
## Method of use

### sever
> docker run -v /home/wang/bwmeasure/bwmur:/app -w /app --net=host --name net_eval net-env:latest python3 /home/onl/bwmur/bwmursever.py

### client
> docker run -v /home/wang/bwmeasure/bwmur:/app -w /app --net=host --name net_eval net-env:latest python3 /home/onl/bwmur/bwmurclient.py
