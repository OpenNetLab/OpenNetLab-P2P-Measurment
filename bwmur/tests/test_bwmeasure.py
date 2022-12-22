#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, pytest, subprocess, time
from tempfile import NamedTemporaryFile


cur_dir = os.path.dirname(os.path.abspath(__file__))


def check_bws():
    file_path = cur_dir + "/../bwmursever.py"
    cmds = ["python3",file_path]
    cmds = (" ".join(cmds))
    subprocess.Popen(cmds,shell = True)
    #os.system(cmds)
    
    
def check_bwc():
    file_path = cur_dir + "/../bwmurclient.py"
    cmdc = ["python3",file_path]
    cmdc = (" ".join(cmdc))
    #cmd_result = subprocess.Popen(cmdc,shell = True).stdout.read()
    cmd_result = os.popen(cmdc).read()
    print(cmd_result)
    assert "scp" in cmd_result



def test_bw():
    check_bws()
    print("OK")
    check_bwc()
