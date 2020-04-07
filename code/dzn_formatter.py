import numpy as np


def array2str(a):
    a = np.array(a)
    s = np.array2string(a, separator=',')
    s = s.replace("],", "")
    s = s.replace("[", "|")
    s = s.replace("]", "|")
    return "[" + s[1:len(s)-1] + "]"

# VENUE_AVAILABILITIES = [|true,true,false,false 
#   |false,false,true,true
#   |true,false,false,true|];

if __name__ == "__main__":
    venues = 5
    periods = 10
    venues_availability = []
    for v in range(venues):
        a = np.random.randint(2, size=periods)
        venues_availability.append(a.astype(bool))

    print(array2str(venues_availability))
    #print(venues_availability)