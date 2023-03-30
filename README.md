# OpenNetLab-P2P-Measurment
## Introduction
For different networks between multiple nodes in the OpenNetLab platform, we hope to have a tool to measure the state of the network environment. OpenNetLab-P2P-Measurement can measure some of the data we design as an objective standard for measuring the network environment.  
## Main measured parameters.    
Bandwidth  
Network Latency   
Jitter  
Packet loss rate  


## Method of use

### Node
> docker run -v /home/wang/bwmeasure/bwmur:/app -w /app --net=host --name net_eval net-env:latest python3 /home/onl/bwmur/bwmur.py



