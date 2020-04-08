import json
import pprint
import os
import dzn_formatter


def create_file(path, content):
    p = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(p):
        os.makedirs(p)
    
    f = open(path, mode='w')
    f.writelines(content)
    f.close()


def export(path, data):    
    dzn = [str(d) + " = " + str(data[d]).replace('\'', '') +  ";\n" for d in data]  
    create_file(path, dzn)

if __name__ == "__main__":
    data = {
        "NB_PERIODS" : "a1",
        "NB_VENUES" : 3,
        "NB_GAMES" : {"q1" : "a4"},
        "NB_TEAMS" : "{a,b}",
        "NB_DIVISIONS" : {"c", "d"}
    }
    export("test.dzn", data)
