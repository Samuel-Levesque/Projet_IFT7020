import subprocess
from threading  import Thread
from os.path import join, abspath, exists, dirname
from os import makedirs
import os
import mmap
import datetime
import sys

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

def excuteMinizinc(pathTomodel, pathToScenario, outputPath, time_to_shut_off, mode='w'):
    try:
        from queue import Queue, Empty
    except ImportError:
        from Queue import Queue, Empty  # python 2.x

    ON_POSIX = 'posix' in sys.builtin_module_names

    def enqueue_output(out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    process = subprocess.Popen(['minizinc', '--solver', 'chuffed', '--verbose-solving', '--solver-statistics', '-f', pathTomodel, pathToScenario], 
                            stdout=subprocess.PIPE,
                            universal_newlines=True,
                            bufsize=1,
                            close_fds=ON_POSIX)

    q = Queue()
    t = Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True # thread dies with the program
    t.start()

    asbsolutpath = dirname(abspath(outputPath))
    if not exists(asbsolutpath):
        makedirs(asbsolutpath)

    print("Saving full result to : " + abspath(outputPath))
    f = open(outputPath, mode)
    begin_time = datetime.datetime.now()
    time_to_shut_off = datetime.timedelta(seconds=time_to_shut_off)
    while True:
        timeDiff = datetime.datetime.now() - begin_time
        
        if(timeDiff >= time_to_shut_off):
            print("Time exceeded : " + str(timeDiff))
            process.kill()
            raise Exception(str(timeDiff))

        # read line without blocking
        try:  line = q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            #print('no output yet')
            a = 1
        else: # got line
            if(line != ''):
                print(line)
                f.writelines(str(line) + '\n')

        return_code = process.poll()
        if return_code is not None:
            #print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            # for output in process.stdout.readlines():
            #     print(output.strip())
            #     f.writelines(str(output.strip()) + '\n')
            break

        # output = process.stdout.readline()
        # print(output.strip())
        # f.writelines(str(output.strip()) + '\n')
        # # Do something else
        # return_code = process.poll()
        # if return_code is not None:
        #     #print('RETURN CODE', return_code)
        #     # Process has finished, read rest of the output 
        #     for output in process.stdout.readlines():
        #         print(output.strip())
        #         f.writelines(str(output.strip()) + '\n')
        #     break
    f.close()
    print("Saving full result to : " + abspath(outputPath) + ". Done.")

    return extractDataToCSV(outputPath)


if(__name__ == "__main__"):
    excuteMinizinc(join('models', 'auto.mzn'), join('test', 'toy-10-4-10-9-[5, 5]-2.dzn'), join('test', 'result.txt'), 1)
