import json
import pprint
import os
import dzn_formatter

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
 
    f.close()


if __name__ == "__main__":
    data = {
        "NB_PERIODS" : "a1",
        "NB_VENUES" : 3,
        "GAME_DURATION" : ["1", "2"],
        "NB_GAMES" : {"q1" : "a4"},
        "NB_TEAMS" : "{a,b}",
        "NB_DIVISIONS" : {"c", "d"}
    }
    export("test.dzn", data)
