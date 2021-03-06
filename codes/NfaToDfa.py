import json
import sys
f = open(sys.argv[1],"r")
nfa=json.load(f)

def getTransitionState(x):
    mp={}
    for y in range(len(x)):
        lis=getlistOfTransitions(x[y])
        for j in lis:
            if j[0] not in mp:
                mp[j[0]]=[]
                temp = len(mp[j[0]])
                tempval = j[1]
                mp[j[0]].insert(temp,tempval)
            else:
                if j[1] not in mp[j[0]]:
                    temp = len(mp[j[0]])
                    tempval = j[1]
                    mp[j[0]].insert(temp,tempval)
    
    return mp


def getlistOfTransitions(xt):
    listt=[]
    global nfa
    
    for k in nfa["transition_function"]:
        if k[0] == xt:
            temp = len(listt)
            templist = [k[1],k[2]]
            listt.insert(temp,templist)
    return listt


dfa={}
dfa["letters"]=nfa["letters"]
dfa["start_states"]=[]
for i in range(len(nfa["start_states"])):
    indx = len(dfa["start_states"])
    dfa["start_states"].insert(indx,[nfa["start_states"][i]])

dfa["states"]=[]
dfa["transition_function"]=[]
dfa["final_states"]=[]

x=len(nfa["states"])
x=2**x
states=[]
for i in range(x):
    pstate=[]
    for j in range(len(nfa["states"])):
        if i & (2**j):
            temp = len(pstate)
            tempval = nfa["states"][j]
            pstate.insert(temp,tempval)
    temp = len(states)
    tempval = pstate
    states.insert(temp,tempval)

for x in states:
    if x == []:
        for t in nfa["letters"]:
            temp = len(dfa["transition_function"])
            tempval = [[],t,[]]
            dfa["transition_function"].insert(temp,tempval)
        continue
    l=getTransitionState(x)
    for key in (l):
        temp = len(dfa["transition_function"]) 
        l[key].sort(key=lambda x:int(x[1:len(x)]))
        # tempval = 
        dfa["transition_function"].insert(temp,[x,key,l[key]])
    for key in nfa["letters"]:
        if key not in l:
            temp = len(dfa["transition_function"])
            tempval = [x,key,[]]
            dfa["transition_function"].insert(temp,tempval)

dfa["states"]=states
finalstates=set({})

for x in nfa["final_states"]:
    for j in dfa["transition_function"]:
        check1 = j[2]
        check2 = j[0]
        if x in check1:
            tempset = set({tuple(j[2])})
            finalstates.update(tempset)
        if x in check2:
            tempset = set({tuple(j[0])})
            finalstates.update(tempset)

finalstates=[list(x) for x in finalstates]
dfa["final_states"]=finalstates
g = open(sys.argv[2],'w')
json.dump(dfa,g,indent=6)