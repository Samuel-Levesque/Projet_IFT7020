import json
import pprint
import os

def _create_dir(outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

def export(path, data):
    dirpath = os.path.dirname(os.path.abspath(path))
    _create_dir(dirpath)
    f = open(path, mode='w')
    for d in data:
        string = str(d) + " = " + str(data[d]).replace('\'', '') +  ";"
        print(string)
        f.writelines(string + "\n")
        #print(type(data[d]))
    f.close()

if __name__ == "__main__":
    data = {
        "d1" : "a1",
        "d2" : 3,
        "d3" : ["1", "2"],
        "d4" : {"q1" : "a4"},
        "d5" : "{a,b}",
        "d6" : {"c", "d"}
    }
    export("test.dzn", data)