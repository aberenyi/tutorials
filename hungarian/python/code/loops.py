#! /usr/bin/env python

# search for loop using connected points of a levelling network
# input file format: startp endp distance height_diff 

import sys

def addp(obs, loop, indx):
    for i in range(indx[-1], len(obs)):
        ob1 = obs[i]
        if ob1[0] == loop[-1] and ob1[1] != loop[-2] and not ob1[1] in loop[1:]:
            # connection to end point
            loop.append(ob1[1])
            indx[-1] = i + 1
            indx.append(0)
            return loop, indx
        if ob1[1] == loop[-1] and ob1[0] != loop[-2] and not ob1[0] in loop[1:]:
            # connection to end point
            loop.append(ob1[0])
            indx[-1] = i + 1
            indx.append(0)
            return loop, indx
    return loop, indx

if len(sys.argv) < 2:
    print ("Usage loops input_file")
    #sys.exit()
    fname = "loops.txt"
else:
    fname = sys.argv[1]
f = open(fname, "r")
obs = []
obs_dic = {}
for line in f:
    l = line.split()
    obs.append(tuple(l))
    obs_dic[l[0] + l[1]] = (float(l[2]), float(l[3]))
loops = []
for ob in obs:
    loop = [ob[0], ob[1]]
    indx = [0, 0]
    while True:
        n = len(loop)
        loop, indx = addp(obs, loop, indx)
        if loop[0] == loop[-1]:
            loops.append(loop[:])   # make a copy of list
            n = len(loop)   # force back step
        if len(loop) == n:
            # no new point or loop found step back
            loop.pop()
            indx.pop()
            indx[-1] += 1
            if len(loop) < 3:
                break
n = 0
m = 0
print (obs_dic)
for i in range(len(loops)):
    # remove duplicates
    loop1 = loops[i]
    n1 = len(loop1)
    s1 = set(loop1)
    for j in range(i+1, len(loops)):
        loop2 = loops[j]
        if n1 == len(loop2) and s1 == set(loop2):
            break   # same route found
    else:
        n += 1
        if m < len(loop1):
            m = len(loop1)
        # calculate height difference & sum distance
        sdist = 0
        sdm = 0
        for i in range(1, len(loop1)):
            if loop1[i-1] + loop1[i] in obs_dic:
                sdist += obs_dic[loop1[i-1] + loop1[i]][0]
                sdm += obs_dic[loop1[i-1] + loop1[i]][1]
            else:
                sdist += obs_dic[loop1[i] + loop1[i-1]][0]
                sdm -= obs_dic[loop1[i] + loop1[i-1]][1]
        print ("%.4f,%7.1f,%s" % (sdm, sdist, loop1))
print (n, m)
