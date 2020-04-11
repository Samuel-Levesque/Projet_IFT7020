import subprocess
from threading  import Thread
from os.path import join, abspath, exists, dirname
from os import makedirs
import os
import mmap
import datetime
import sys

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

def excuteMinizinc(pathTomodel, pathToScenario, outputPath, time_to_shut_off, mode='w'):
    #processCompile = subprocess.Popen(['minizinc', '-c', '--solver', 'chuffed', pathTomodel, pathToScenario], stdout=subprocess.PIPE, universal_newlines=True)
    print("Compiling model : " + pathTomodel)
    os.system('minizinc -c -v --solver chuffed "' + pathTomodel + '" "' + pathToScenario +  '"')
    print("Done compiling model : " + pathTomodel)
    # while True:
    #     output = processCompile.stdout.readline()
    #     if(output.strip() != ''):
    #         print(output.strip())
    #     # Do something else
    #     return_code = processCompile.poll()
    #     if return_code is not None:
    #         #print('RETURN CODE', return_code)
    #         # Process has finished, read rest of the output 
    #         for output in processCompile.stdout.readlines():
    #             if(output.strip() != ''):
    #                 print(output.strip())
    #         break

    pathToFZN = pathTomodel[:len(pathTomodel)-3] + 'fzn'
    pathToOZN = pathTomodel[:len(pathTomodel)-3] + 'ozn'
    process = subprocess.Popen(['minizinc', '--solver', 'chuffed', '-a', '--verbose-solving', '--solver-statistics', '-f', '--solver-time-limit', str(time_to_shut_off), pathToFZN], stdout=subprocess.PIPE, universal_newlines=True)

    asbsolutpath = dirname(abspath(outputPath))
    if not exists(asbsolutpath):
        makedirs(asbsolutpath)

    print("Saving full result to : " + abspath(outputPath))
    f = open(outputPath, mode)
    while True:
        output = process.stdout.readline()
        if(output.strip() != ''):
            print(output.strip())
            f.writelines(str(output.strip()) + '\n')
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            #print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                if(output.strip() != ''):
                    print(output.strip())
                    f.writelines(str(output.strip()) + '\n')
            break
    f.close()
    print("Saving full result to : " + abspath(outputPath) + ". Done.")

    return extractDataToCSV(outputPath, time_to_shut_off)


if(__name__ == "__main__"):
    excuteMinizinc(join('models', 'auto.mzn'), join('test', 'toy-40-20-60-60-[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]-2.dzn'), join('models', 'result.txt'), 1*1000)
