import subprocess
from os.path import join, abspath

def excuteMinizinc(pathTomodel, pathToScenario, outputPath, mode='w'):
    process = subprocess.Popen(['minizinc', '--solver', 'chuffed', '--verbose-solving', '--solver-statistics', '-f', pathTomodel, pathToScenario], 
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

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
    print("Saving result to : " + abspath(outputPath))
    f.close()


if(__name__ == "__main__"):
    excuteMinizinc(join('models', 'model2.mzn'), join('models', 'scenario 2.dzn'), join('models', 'result.txt'))
