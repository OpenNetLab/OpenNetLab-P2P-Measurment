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
server_port = "8000"
server_ip = "0.0.0.0"

server_run_cmd = [
    "iperf3 -s -p %s -i 1 -1" % (
        server_port)]
client_run_cmd = [
    "iperf3 -c %s -p %s" % (
        server_ip, server_port)]

def get_datetime():
    now = int(round(time.time() * 1000))
    ret = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
    return ret
    

def get_bw(name):
    global server_ip
    global server_port
    with open(machines_file, 'r') as f:
        machines = json.loads(f.read())
        if name not in machines:
            raise ValueError("Not find such mahcine")
        _ip = machines[name]["host"]
        _port = machines[name]["bw_port"]
        
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
        output =" "
        get_bw("recv_%d" % (matches_num))
        _run_cmd = ["iperf3 -s -p %s -i 1 " % (_port)]
        print(" ".join(_run_cmd))
        status = os.popen(" ".join(_run_cmd)).read()
        cmd = _run_cmd
        doc = open('bwlog.txt', 'a+')
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
