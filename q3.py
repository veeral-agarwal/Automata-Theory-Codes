import json
from copy import deepcopy
import sys

def calinout(intermediateStates):
    global dfa
    mp=[]
    for x in range(len(intermediateStates)):
        ie=0
        oe=0
        for j in range(len(dfa["transition_function"])):
            if dfa["transition_function"][j][2] == intermediateStates[x]:
                ie+=1
            elif dfa["transition_function"][j][0] == intermediateStates[x]:
                oe+=1
        mp.append([intermediateStates[x],(ie,oe)])
    mp.sort(key=lambda a:a[1][0]+a[1][1])
    ie=0
    oe=0
    return mp

def getAllTransitions(xt):
    global dfa
    outgoing=[]
    selfloop=[]
    lis=[]
    incoming=[]
    
    for x in range(len(dfa["transition_function"])):
        if xt in dfa["transition_function"][x]:
            lis.append(dfa["transition_function"][x])
    
    for x in range(len(lis)):
        if xt == lis[x][0] and xt!=lis[x][2]:
            outgoing.append(lis[x])
        elif xt == lis[x][2] and xt!=lis[x][0]:
            incoming.append(lis[x])
        else:
            selfloop.append(lis[x])
    return incoming,outgoing,selfloop

def clearOldTransitions(r):
    global dfa
    for x in range(len(r)):
        if r[x] in dfa["transition_function"]:
            dfa["transition_function"].remove(r[x])

f = open(sys.argv[1],"r")
dfa=json.load(f)
if len(dfa["final_states"])>1:
    for x in range(len(dfa["final_states"])):
        indx = len(dfa["transition_function"])
        val = [dfa["final_states"][x],'$','Qf']
        dfa["transition_function"].insert(indx,val)
    
    dfa["final_states"]=["Qf"]

startstate=dfa["start_states"][0]
for x in range(len(dfa["transition_function"])):
    if startstate == dfa["transition_function"][x][2]:
        indx = len(dfa["transition_function"])
        val = ["Qi","$",startstate]
        dfa["transition_function"].insert(indx,val)
        startstate="Qi"
        dfa["start_states"][0]="Qi"
        break

finalstate=dfa["final_states"][0]
for x in range(len(dfa["transition_function"])):
    if finalstate == dfa["transition_function"][x][0]:
        indx = len(dfa["transition_function"])
        val = [finalstate,"$","Qf"]
        dfa["transition_function"].insert(indx,val)
        dfa["final_states"]=["Qf"]
        break

intermediateStates=deepcopy(dfa["states"])
check1 = dfa['start_states'][0]
if check1 in intermediateStates:
    intermediateStates.remove(check1)
check2 = dfa['final_states'][0]
if check2 in intermediateStates:
    intermediateStates.remove(check2)
ieedges = calinout(intermediateStates)
sizeinterm = len(intermediateStates)

sizetrans = len(dfa["transition_function"])
while sizetrans !=1 and sizeinterm>0:
    exp=[]
    stateToRemove=ieedges[0][0]
    inc,out,selfloops=getAllTransitions(stateToRemove)
    
    if len(selfloops) > 1:
        exp=[]
        for lo in range(len(selfloops)):
            indx = len(exp)
            val = selfloops[lo][1]
            exp.insert(indx , val )
            indx = len(exp)
            exp.insert(indx,'+')
        indx = len(exp)-1
        exp.pop(indx)
        exp=''.join(exp)

    if len(selfloops) == 1:
        exp=selfloops[0][1]
    if len(selfloops)<1:
        exp=''
    for x in range(len(inc)):
        for y in range(len(out)):
            if exp == "":
                indx = len(dfa["transition_function"])
                val = [inc[x][0],"{}{}".format(inc[x][1],out[y][1]),out[y][2]]
                dfa["transition_function"].insert(indx,val)
            elif len(exp) == 1:
                indx = len(dfa["transition_function"])
                val = [inc[x][0],"{}{}*{}".format(inc[x][1],exp,out[y][1]),out[y][2]]
                dfa["transition_function"].insert(indx,val)
            else:
                indx = len(dfa["transition_function"])
                val = [inc[x][0],"{}({})*{}".format(inc[x][1],exp,out[y][1]),out[y][2]]
                dfa["transition_function"].insert(indx,val)
    
    for x in range(len(out)):
        if out[x] in dfa["transition_function"]:
            dfa["transition_function"].remove(out[x])
    for x in range(len(inc)):
        if inc[x] in dfa["transition_function"]:
            dfa["transition_function"].remove(inc[x])
    for x in range(len(selfloops)):
        if selfloops[x] in dfa["transition_function"]:
            dfa["transition_function"].remove(selfloops[x])

    intermediateStates.remove(stateToRemove)
    ieedges = calinout(intermediateStates)
    # ieedges.sort(key=lambda a:a[1][0]+a[1][1])
    sizeinterm = len(intermediateStates)
    sizetrans = len(dfa["transition_function"])

fg=[]
finalregex = []

for x in range(len(dfa["transition_function"])):
    indx = len(fg)
    val = dfa["transition_function"][x][1]
    fg.insert(indx , val)
    fg.insert(len(fg),'+')

if len(fg)>0:
    indx = len(fg)-1
    fg.pop(indx)
fg=''.join(fg)
fromm = dfa["transition_function"][0][0]
to = dfa["transition_function"][0][2]
dfa["transition_function"] = [[fromm,fg,to]]

for x in range(len(dfa["transition_function"][0][1])):
    if dfa["transition_function"][0][1][x]!='$':
        finalregex.append(dfa["transition_function"][0][1][x])
regex={}
regex['regex']=''.join(finalregex)
g = open(sys.argv[2],'w')

json.dump(regex,g)