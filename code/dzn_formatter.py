import numpy as np


def array2str(a, remove_str_chars=True):
    a = np.array(a)
    s = np.array2string(a, separator=',')
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

# VENUE_AVAILABILITIES = [|true,true,false,false
#   |false,false,true,true
#   |true,false,false,true|];

if __name__ == "__main__":
#    venues = 5
#    periods = 10
#    venues_availability = []
#    for v in range(venues):
#        a = np.random.randint(2, size=periods)
#        venues_availability.append(a.astype(bool))
#
#    print(array2str(venues_availability))
#    print(venues_availability)

    ls = ['Div_1_Team_1', 'Div_1_Team_2', 'Div_1_Team_3', 'Div_2_Team_1', 'Div_2_Team_2', 'Div_2_Team_3']
#    print(list2enum_str(ls))

    a = np.array([[0, 0, 0, 0], [1, 0, 0, 0,], [0, 0, 0, 0], [0, 1, 4, 0], [0, 0, 1, 0], [0, 3, 5, 0]])
    print(array2array2d(a))