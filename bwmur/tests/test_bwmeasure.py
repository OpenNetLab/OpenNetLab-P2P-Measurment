#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, pytest, subprocess, time
from tempfile import NamedTemporaryFile


cur_dir = os.path.dirname(os.path.abspath(__file__))


def check_bw():
    file_path = cur_dir + "/../bwmeasure.py"
    cmd = ["python3", file_path]
    print(cmd)
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    print(cmd_result)
    data = cmd_result.stdout
    assert "Bitrate" in data



def test_bw():
    check_bw()