import subprocess
from os.path import join, abspath, exists, dirname
from os import makedirs
import os
import mmap

def extractDataToCSV(outputPath):

    unsatisfiable = True
    stringtime = ""
    stringnode = ""
    stringnogood = ""
    with open(outputPath) as f:
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if(s.find(b'=====UNSATISFIABLE=====') != -1):
            #print("The scenario is unsatisfiable.")
            unsatisfiable = True
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

def excuteMinizinc(pathTomodel, pathToScenario, outputPath, mode='w'):
    process = subprocess.Popen(['minizinc', '--solver', 'chuffed', '--verbose-solving', '--solver-statistics', '-f', pathTomodel, pathToScenario], 
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    asbsolutpath = dirname(abspath(outputPath))
    if not exists(asbsolutpath):
        makedirs(asbsolutpath)

    print("Saving full result to : " + abspath(outputPath))
    f = open(outputPath, mode)
    while True:
        output = process.stdout.readline()
        print(output.strip())
        f.writelines(str(output.strip()) + '\n')
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            #print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                print(output.strip())
                f.writelines(str(output.strip()) + '\n')
            break
    f.close()
    print("Saving full result to : " + abspath(outputPath) + ". Done.")

    return extractDataToCSV(outputPath)


if(__name__ == "__main__"):
    excuteMinizinc(join('models', 'model2.mzn'), join('models', 'scenario2.dzn'), join('test', 'result.txt'), "outputcsv.csv")
