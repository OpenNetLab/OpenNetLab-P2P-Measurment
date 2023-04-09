import paramiko
import time
import random
import json
import os
import sys
from scp import SCPClient
import numpy as np
import copy
import time

socket_timeout_sec = 240
machines_file = "machines.json"
sever_port = "8000"
sever_ip = "20.81.187.38"
recv_wd = "/home/wang/testnet/"

sever_run_cmd = [
    "iperf3 -s -p %s -i 1 -1" % (
        sever_port)]
client_run_cmd = [
    "iperf3 -c %s -p %s" % (
        sever_ip, sever_port)]

def get_datetime():
    now = int(round(time.time() * 1000))
    ret = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
    return ret
    

def get_bw(name):
    global sever_ip
    global sever_port
    with open(machines_file, 'r') as f:
        machines = json.loads(f.read())
        if name not in machines:
            raise ValueError("Not find such mahcine")
        sever_ip = machines[name]["host"]
        sever_port = machines[name]["bw_port"]
        
def get_ssh(name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    with open(machines_file, 'r') as f:
        machines = json.loads(f.read())
        if name not in machines:
            raise ValueError("Not find such mahcine")

        client.connect(hostname=machines[name]["host"], port=machines[name]["ssh_port"], username=machines[name]["user"],
                       password=machines[name]["pwd"])
    return client

def BWmeasure(matches_num):
    try:
        output = " "
        get_bw("recv_%d" % (matches_num))
        sever_run_cmd = ["iperf3 -s -p %s -i 1 " % (sever_port)]
        print(" ".join(sever_run_cmd))
        status = os.popen(" ".join(sever_run_cmd)).read()
        cmd = sever_run_cmd
        doc = open('severbwlog.txt', 'a+')
        doc.seek(0)
        doc.truncate()
        doc.write(status)
        doc.close()
    except Exception as e:
        print(get_datetime(), "run_measure", e)
    finally:
        print("measure finish")

if __name__ == "__main__":
    BWmeasure(1)
