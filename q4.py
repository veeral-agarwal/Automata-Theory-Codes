import json
import sys
from copy import deepcopy
f = open(sys.argv[1],"r")
dfa=json.load(f)

for x in range(len(dfa["states"])):
    ie=0
    oe=0
    for j in dfa["transition_function"]:
        if dfa["states"][x] == j[2]:
            ie+=1
        elif dfa["states"][x]==j[0]:
            oe+=1
    if oe==0 and dfa["states"][x] not in dfa["final_states"]:
        toremove=[]
        for y in range(0,len(dfa["transition_function"])):
            if dfa["states"][x] in dfa["transition_function"][y]:
                toremove.append(dfa["transition_function"][y])
        for i in range(0,len(toremove)):
            dfa["transition_function"].remove(toremove[i])
        dfa["states"].remove(dfa["states"][x])
        if dfa["states"][x] in dfa["final_states"]:
            dfa["final_states"].remove(dfa["states"][x])


def distinctcheck(x,y):
    global dfa
    global mp1
    global mp2
    global transition_table
    for xt in range(len(dfa["letters"])):
        x1=transition_table[mp2[x]][mp1[dfa["letters"][xt]]]
        x2=transition_table[mp2[y]][mp1[dfa["letters"][xt]]]
        global previousp1
        for i in range(len(previousp1)):
            if x1 in previousp1[i]:
                x1=i
        for i in range(len(previousp1)):
            if x2 in previousp1[i]:
                x2=i
        if x1!=x2:
            return True
    return False

def partition(x):
    mp={}
    stateToRemove=[]

    for i in range(len(x)):
        mp[x[i]]=0
    for i in range(len(x)):
        for j in range(i+1,len(x),1):
            
            if distinctcheck(x[i],x[j]):
                mp[x[j]]+=1
                mp[x[i]]+=1
                
    stateToRemove.clear()
    u=0
    for i in mp:
        if mp[i]>u:
            u=mp[i]
    for i in range(0,len(x)):
        if mp[x[i]] == u:
            indx = len(stateToRemove)
            stateToRemove.insert(indx,x[i])
    templist = []
    for xt in x :
        if xt not in stateToRemove:
            templist.append(xt)
    return templist,stateToRemove
def transstate(x,y):
    global previousp,previousp1,mp1,transition_table
    
    
    global mp2
    for i in range(len(previousp1)):
        check = previousp1[i]
        if transition_table[mp2[x]][mp1[y]] in check:
            return previousp[i]

def transitioneqornot(x):
    mp={}
    global mp2
    global transition_table
    

    for xt in range(len(x)):
        tt=[str(r) for r in transition_table[mp2[x[xt]]]]
        exp=''.join(tt)
        if exp in mp:
            mp[exp].append(x[xt])
        else:
            mp[exp]=[x[xt]]
    fs=[]
    for key in mp:
        indx = len(fs)
        fs.insert(indx,mp[key])
    return fs 
mp1={}
start=0
transition_table = [['$' for x in dfa["letters"]] for y in dfa["states"]]


for i in range(len(dfa["letters"])):
    mp1[dfa["letters"][i]]=start
    start+=1
start=0
mp2={}
for i in range(0,len(dfa['states'])):
    mp2[dfa['states'][i]]=start
    start+=1
for x in range(0,len(dfa['transition_function'])):
    transition_table[mp2[dfa['transition_function'][x][0]]][mp1[dfa['transition_function'][x][1]]]=mp2[dfa['transition_function'][x][2]]

previousp=[]
p0=[]
startstates=dfa["states"]
for x in range(len(dfa["final_states"])):
    startstates.remove(dfa["final_states"][x])
startstates=transitioneqornot(startstates)
l=transitioneqornot(dfa["final_states"])
p0=startstates
for i in range(len(l)):
    indx = len(p0)
    p0.insert(indx,l[i])
p=0
previousp=p0
nextstate = []     
while 1:
    p+=1
    nextstate.clear()
    previousp1=deepcopy(previousp)
    for x in range(len(previousp1)):
        for y in range(len(previousp1[x])):
            check = previousp1[x][y] 
            previousp1[x][y]=mp2[check]
    for x in range(len(previousp)):
        s1,s2=partition(previousp[x])
        if s2 == []:
            indx = len(nextstate)
            nextstate.insert(indx,s1)
        elif s1 == []:
            indx=len(nextstate)
            nextstate.insert(indx,s2)
        else:
            indx=len(nextstate)
            nextstate.insert(indx,s1)
            nextstate.insert(indx+1,s2)
    
    if nextstate in [previousp]:
        break
    else:
        previousp=deepcopy(nextstate)
        nextstate.clear()

newdfa={}
newdfa['states']=previousp
newdfa['start_states']=[]
newdfa['final_states']=[]
newdfa['letters']=dfa['letters']
newdfa['transition_function'] = []
ss=[]
fs=[]
for i in range(len(dfa['start_states'])):
    for j in range(len(previousp)):
        if (dfa['start_states'][i] in previousp[j]) and (previousp[j] not in ss):
            ss.append(previousp[j])
for i in range(len(dfa['final_states'])):
    for j in range(len(previousp)):
        if (dfa['final_states'][i] in previousp[j]) and (previousp[j] not in fs):
            fs.append(previousp[j])
for i in range(len(previousp)):
    for j in range(len(dfa['letters'])):
        u=transstate(previousp[i][0],dfa['letters'][j])
        if u:
            newdfa["transition_function"].append([previousp[i],dfa['letters'][j],u])

newdfa['start_states']=ss
newdfa['final_states']=fs

g = open(sys.argv[2],"w") 
json.dump(newdfa,g,indent=6)