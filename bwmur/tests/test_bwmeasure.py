#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, pytest, subprocess, time
from tempfile import NamedTemporaryFile


cur_dir = os.path.dirname(os.path.abspath(__file__))


def check_bws():
    file_path = cur_dir + "/../bwmeasure.py"
    cmds = "iperf3 -s -1"
    subprocess.Popen(cmds,shell = True)
    #os.system(cmds)
    
    
def check_bwc():
    cmdc = "iperf3 -c 127.0.0.1 -t 5"
    #cmd_result = subprocess.Popen(cmdc,shell = True).stdout.read()
    cmd_result = os.popen(cmdc).read()
    print(cmd_result)
    assert "Bitrate" in cmd_result



def test_bw():
    check_bws()
    print("OK")
    check_bwc()
