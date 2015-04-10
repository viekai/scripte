#!/usr/bin/env python
import os
import time
import os
import time
import sys
import subprocess
import datetime
import signal
import select
import thread
from threading import Timer
# coding=utf-8
import zipfile
import sys
import time

def execute2(args):
     p = subprocess.Popen(args.split(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
     return p.returncode, p.stdout

def executeWait(args):
     p = subprocess.Popen(args.split(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
     p.wait();
     return p.returncode, p.stdout

free_data = []
used_data = []
name_data_map = {"Free RAM":free_data, "Used RAM":used_data}

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print "Need file name :  ./getStartMem.py startFile"
    fileName = sys.argv[1];
    fd = open(fileName, "w");
    for i in range(0, 6) :
        fileName = fileName + str(i)
        ret, out = execute2("adb shell reboot");
        print("Reboot... ");
        time.sleep(60*5);
        print("Reboot ok ... ");
        i = 100 

        for name in name_data_map.keys():
            name_data_map[name] = [];

        while(i > 0):
            ret, out = execute2("adb shell dumpsys meminfo |grep RAM");
            for info in out:
                name_data = info.split(":"); 
                name = info.split(":")[0].strip(":").strip();
                data = info.split(":")[-1].split("kB")[0];
                if (name in name_data_map.keys()):
                    name_data_map[name].append(data);
            time.sleep(1);
            i = i -1;

        print("Writing file....");

        for name in name_data_map.keys():
            fd.write(name + "_" + fileName + " ")
            for item in name_data_map[name]:
                fd.write(item + " ");
            fd.write("\n");

    fd.close();
