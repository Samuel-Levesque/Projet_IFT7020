import subprocess
from threading  import Thread
from os.path import join, abspath, exists, dirname
from os import makedirs
import os
import mmap
import datetime
import sys
from dzn_export import create_file

def extractDataToCSV(outputPath, time_to_shut_off):

    unsatisfiable = True
    stringtime = ""
    stringnode = ""
    stringnogood = ""
    with open(outputPath) as f:
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if(s.find(b'=====UNSATISFIABLE=====') != -1):
            #print("The scenario is unsatisfiable.")
            unsatisfiable = True
        elif(s.find(b'% Time limit exceeded!') != -1):
            raise Exception(str(time_to_shut_off))
        else:
            unsatisfiable = False
            f.seek(0, os.SEEK_SET)
            for line in f.readlines():
                time = line.find("%%%mzn-stat: time=")
                node = line.find("%%%mzn-stat: nodes=")
                nogood = line.find("%%%mzn-stat: nogoods=")
                slashn = line.find("\n")
                if(time != -1):
                    stringtime = line[len("%%%mzn-stat: time="): slashn]
                if(node != -1):
                    stringnode = line[len("%%%mzn-stat: nodes="): slashn]
                if(nogood != -1):
                    stringnogood = line[len("%%%mzn-stat: nogoods="): slashn]
    
    return unsatisfiable, stringtime, stringnode, stringnogood

def excuteMinizinc(path2model, path2Scenario, outputPath, timeout):

    parms = [
        'C:/Program Files/MiniZinc/minizinc.exe',
        '--solver', 
        'chuffed', 
        '-a', 
        '--verbose-solving', 
        '--solver-statistics', 
        '-f', 
        '--solver-time-limit', 
        str(timeout), 
        path2model, 
        path2Scenario
    ]
    
    out, err = subprocess.Popen(parms, stdout=subprocess.PIPE, universal_newlines=True).communicate() 

    create_file(outputPath, out)
  
    return extractDataToCSV(outputPath, timeout)
