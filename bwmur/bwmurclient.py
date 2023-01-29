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
sever_ip = "127.0.0.1"
recv_wd = "/home"

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
        print(machines[name]["host"])
        print(sever_ip)
        

        
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
        client_run_cmd = ["iperf3 -c %s -p %s" % (sever_ip, sever_port)]
        status = os.popen(" ".join(client_run_cmd)).read()
        print(" ".join(client_run_cmd))
        cmd = client_run_cmd
        doc = open('clientbwlog.txt', 'a+')
        doc.seek(0)
        doc.truncate()
        doc.write(status)
        doc.close()
        netctr = get_ssh("netctr")
        print("start scp")
        scp_client = SCPClient(netctr.get_transport(), socket_timeout=30.0)
        scp_client.put("clientbwlog.txt", "%s/." % (recv_wd))
        scp_client.close()


    except Exception as e:
        print(get_datetime(), "run_measure", e)

    finally:
        print("measure finish")

if __name__ == "__main__":
    BWmeasure(1)
