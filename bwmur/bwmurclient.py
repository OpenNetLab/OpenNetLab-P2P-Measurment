import time
import random
import json
import os
import sys
import re
import copy
import time

socket_timeout_sec = 240
machines_file = "machines.json"
server_port = "8000"
server_ip = "127.0.0.1"
tcpbw = 0.0
proportion = 11

server_run_cmd = [
    "iperf3 -s -p %s -i 1 -1" % (
        server_port)]
client_run_cmd = [
    "iperf3 -c %s -p %s" % (
        server_ip, server_port)]
        
latency_mur_cmd = [
    "ping -c 4 %s" % (
    server_ip)]

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
        server_ip = machines[name]["host"]
        server_port = machines[name]["bw_port"]
        print(machines[name]["host"])
        print(server_ip)
                
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

# Bandwidth measurement program
# Use Iperf3's TCP mode to measure network bandwidth
# Using Iperf's UDP mode to measure between 10% and 100%
def BWmeasure(matches_num):
    global tcpbw
    try:
        output =" "
        get_bw("recv_%d" % (matches_num))
        client_run_cmd = ["iperf3 -c %s -p %s -f M" % (server_ip, server_port)]
        print(" ".join(client_run_cmd))
        status = os.popen(" ".join(client_run_cmd)).read()
        cmd = client_run_cmd
        doc = open('clientbwlog.txt', 'a+')
        doc.seek(0)
        doc.truncate()
        doc.write(get_datetime())
        doc.write("\n")
        doc.write(" ".join(client_run_cmd))
        doc.write("\n")
        doc.write(status)
        doc.close()
        sta = status.split('\n')
        data = {}
        for it in sta:
            if it == None:
                continue
            pattern = re.compile('[  5].*?receiver')
            if pattern.search(it) != None :
                result = pattern.search(it).group()
                tcpbw = float(result.split()[5])
                tcpstr = result.split()[6]
                data["bandwidth"] = float(result.split()[5])
                data["time"] = get_datetime()
        ltcstatus = os.popen(" ".join(latency_mur_cmd)).read()
        doc = open('clientbwlog.txt', 'a+')
        doc.write(get_datetime())
        doc.write("\n")
        doc.write(" ".join(latency_mur_cmd))
        doc.write("\n")
        doc.write(ltcstatus)
        for i in range(1,proportion):
            print(i)
            print("iperf3 -u -c %s -b %s -p %s" %(server_ip, str(round(tcpbw*i*0.1,2))+tcpstr[0], server_port))
            doc.write(get_datetime())
            doc.write("\n")
            doc.write("iperf3 -u -c %s -b %s -p %s" %(server_ip, str(round(tcpbw*i*0.1,2))+tcpstr[0], server_port))
            doc.write("\n")
            bw_status = os.popen("iperf3 -u -c %s -b %s -p %s" %(server_ip, str(tcpbw*i*0.1)+tcpstr[0], server_port)).read()
            doc.write(bw_status)
            bw_ss = bw_status.split()
            data[str(round(i*0.1,2)) + "_Jitter_Sender" ] = float(bw_ss[155])
            print(float(bw_ss[158].strip("()%")))
            data[str(round(i*0.1,2)) + "_Packet-loss-rate_Sender" ] = float(bw_ss[158].strip("()%"))
            data[str(round(i*0.1,2)) + "_Jitter_Receiver" ] = float(bw_ss[168])
            data[str(round(i*0.1,2)) + "_Packet-loss-rate_Receiver" ] =  float(bw_ss[171].strip("()%"))
        with open(machines_file, 'r') as f:
            machines = json.loads(f.read())
            data["machines"] = machines
        with open("data.json", "w") as f:
            data["time"] = get_datetime()
            json_data = json.dumps(data)
            f.write(json_data)
        doc.close()
    except Exception as e:
        print(get_datetime(), "run_measure", e)
    finally:
        print("measure finish")

if __name__ == "__main__":
    BWmeasure(1)
