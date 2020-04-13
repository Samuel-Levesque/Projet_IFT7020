import numpy as np
import sys

def array2str(a, remove_str_chars=True):
    np.set_printoptions(threshold=sys.maxsize)
    a = np.array(a)
    s = np.array2string(a, separator=',')
    s = s.lower()
    s = s.replace("],", "")
    s = s.replace("[", "|")
    s = s.replace("]", "|")
    if remove_str_chars:
        s = s.replace("b'", "")
        s = s.replace("'", "")
    return "[" + s[1:len(s)-1] + "]"

def list2enum_str(ls):
    ls = str(ls)
    ls = ls.replace("'", "")
    ls = ls.replace("[", "{")
    ls = ls.replace("]", "}")
    return ls

def array2array2d(a):
    np.set_printoptions(threshold=sys.maxsize)
    s = np.array2string(a)
    s = s.replace("[[", "__")
    s = s.replace("]]", "--")
    s = s.replace("[", "")
    s = s.replace("]", ",")
    s = s.replace("__", "[")
    s = s.replace("--", "]")
    s = s.replace(" ", ",")
    s = s.replace("\n,", "\n")

    return f"array2d(TEAM_NAMES, periods, {s})"

if __name__ == "__main__":
    ls = ['Div_1_Team_1', 'Div_1_Team_2', 'Div_1_Team_3', 'Div_2_Team_1', 'Div_2_Team_2', 'Div_2_Team_3']
    a = np.array([[0, 0, 0, 0], [1, 0, 0, 0,], [0, 0, 0, 0], [0, 1, 4, 0], [0, 0, 1, 0], [0, 3, 5, 0]])
    print(array2array2d(a))
