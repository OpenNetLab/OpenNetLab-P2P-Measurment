# OpenNetLab-P2P-Measurment

## Introduction
For different networks between multiple nodes in the OpenNetLab platform, we hope to have a tool to measure the state of the network environment. OpenNetLab-P2P-Measurement can measure some of the data we design as an objective standard for measuring the network environment.


## Main measured parameters  
| Type     | Definition    |
| -------- | -------- |
| 1. Bandwidth | Iperf3 TCP mode & Iperf3 UDP mode (2x TCP result and see received throughout) |
| 2. Network Latency | Iperf3 UDP mode (use Bandwidth in 1%,10% ,…, 100% Bandwidth) |
| 3. Jitter | Iperf3 UDP mode (use Bandwidth in 1%,10% ,…, 100% Bandwidth) |
| 4. Packet loss rate | Iperf3 UDP mode (use Bandwidth in 1%,10% ,…, 100% Bandwidth) |  

## Usage method  

### sever
> docker run -v /home/wang/bwmeasure/bwmur:/app -w /app --net=host --name net_eval net-env:latest python3 /home/onl/bwmur/bwmursever.py

### client
> docker run -v /home/wang/bwmeasure/bwmur:/app -w /app --net=host --name net_eval net-env:latest python3 /home/onl/bwmur/bwmurclient.py

## Running results  
Contains two files, data.json and clientbwlog.txt. The data.json file format stores the numerical values of the results, while the clientbwlog.txt file contains the log information during the measurement process.
