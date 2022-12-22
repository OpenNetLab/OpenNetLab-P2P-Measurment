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
    "iperf3 -s -p %s -i 1" % (
        sever_port)]
client_run_cmd = [
    "iperf3 -c %s -p %s" % (
        sever_ip, sever_port)]


def get_datetime():
    now = int(round(time.time() * 1000))
    ret = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
    return ret


def get_ssh(name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    with open(machines_file, 'r') as f:
        machines = json.loads(f.read())
        if name not in machines:
            raise ValueError("Not find such mahcine")

        client.connect(hostname=machines[name]["host"], port=machines[name]["ssh_port"], username=machines[name]["user"],
                       password=machines[name]["pwd"])

        #print(machines[name]["host"])
        #print(machines[name]["ssh_port"])
        #print(machines[name]["user"])

    return client

def get_bw(name):
    global sever_ip
    global sever_port
    with open(machines_file, 'r') as f:
        machines = json.loads(f.read())
        if name not in machines:
            raise ValueError("Not find such mahcine")

        #print("iperf")
        #print(machines[name]["host"])
        #print(machines[name]["bw_port"])
        sever_ip = machines[name]["host"]
        sever_port = machines[name]["bw_port"]

        



def BWmeasure(matches_num):
    #print(get_datetime(), "start measure")
    try:
        sender = get_ssh("sender_%d" % (matches_num))
        recv = get_ssh("recv_%d" % (matches_num))
        get_bw("recv_%d" % (matches_num))
        shell_sender, shell_recv = sender.invoke_shell(), recv.invoke_shell()
        shell_sender.settimeout(socket_timeout_sec)
        shell_recv.settimeout(socket_timeout_sec)

        # shell_sender.send("sudo su\n")
        # shell_recv.send("sudo su\n")
        # time.sleep(3)
        output =" "

        def start_recv():
            #print(get_datetime(), "start recv")
            cmd = sever_run_cmd
            #print(' '.join(cmd))
            shell_recv.send(' '.join(cmd) + "\n")
            # time.sleep(1000)

        def start_sender():
            output = " "
            #print(get_datetime(), "start sender")

            cmd = client_run_cmd
            #print(get_datetime(), ' '.join(cmd))
            shell_sender.send(' '.join(cmd) + "\n")
            times=0
            doc = open('bwlog.txt', 'a+')
            doc.seek(0)
            doc.truncate()
            doc.close()
            while times < 15:
                time.sleep(1)
                times += 1
                if times <2:
                    if shell_sender.recv_ready():
                        outbuf = shell_sender.recv(65535)
                    continue
                if shell_sender.recv_ready():
                    outbuf = shell_sender.recv(65535)
                    if len(outbuf) == 0:
                        break
                    output += outbuf.decode("utf-8", "ignore")
                    doc = open('bwlog.txt', 'a+')
                    doc.write(outbuf.decode("utf-8", "ignore"))
                    doc.close()
            print(output)
        start_recv()
        time.sleep(1)
        print("signal signal")
        start_sender()
        netctr = get_ssh("netctr")
        print("start scp")
        scp_client = SCPClient(netctr.get_transport(), socket_timeout=30.0)
        scp_client.put("bwlog.txt", "%s/." % (recv_wd))
        scp_client.close()


    except Exception as e:
        print(get_datetime(), "run_measure", e)

    finally:
        print("measure finish")

if __name__ == "__main__":
    BWmeasure(1)
