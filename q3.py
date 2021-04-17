import json
from copy import deepcopy

def calculateIncomingAndOutgoingEdges(intermediateStates):
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

f = open('./dfa1.json')
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
if dfa["start_states"][0] in intermediateStates:
    intermediateStates.remove(dfa["start_states"][0])
if dfa["final_states"][0] in intermediateStates:
    intermediateStates.remove(dfa["final_states"][0])
ieedges = calculateIncomingAndOutgoingEdges(intermediateStates)
ieedges.sort(key=lambda a:a[1][0]+a[1][1])
while len(dfa["transition_function"])!=1 and len(intermediateStates)>0:
    print(dfa["transition_function"])
    stateToRemove=ieedges[0][0]
    inc,out,selfloops=getAllTransitions(stateToRemove)
    print(selfloops)
    exp=[]
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
        # dfa["transition_function"].append([stateToRemove,exp,stateToRemove])
    elif len(selfloops) == 1:
        exp=selfloops[0][1]
    else:
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
    clearOldTransitions(inc)
    clearOldTransitions(out)
    clearOldTransitions(selfloops)
    # print(stateToRemove)
    intermediateStates.remove(stateToRemove)
    ieedges = calculateIncomingAndOutgoingEdges(intermediateStates)
    ieedges.sort(key=lambda a:a[1][0]+a[1][1])

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
print(fg)
print(dfa["transition_function"])
fromm = dfa["transition_function"][0][0]
to = dfa["transition_function"][0][2]
dfa["transition_function"] = [[fromm,fg,to]]
print(dfa["transition_function"])
for x in range(len(dfa["transition_function"][0][1])):
    if dfa["transition_function"][0][1][x]!='$':
        finalregex.append(dfa["transition_function"][0][1][x])
regex={}
regex['regex']=''.join(finalregex)
g = open('./outregex.json','w')
json.dump(regex,g)