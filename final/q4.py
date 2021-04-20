import json
from copy import deepcopy
from sys import argv

f = open(argv[1])
dfa=json.load(f)

# flag=False
# while flag == False:
#     # print("htrt")
#     for x in dfa["states"]:
#         ie=oe=0
#         for j in dfa["transition_function"]:
#             if x==j[0] and x == j[2]:
#                 pass
#             elif x == j[2]:
#                 ie+=1
#             elif x==j[0]:
#                 oe+=1
#         if (ie ==0 and oe ==0):
#             if x in dfa['states']:
#                 dfa["states"].remove(x)
#             if x in dfa["final_states"]:
#                 dfa["final_states"].remove(x)
#             if x in dfa["start_states"]:
#                 dfa["start_states"].remove(x)
#                 # flag=True
#                 # break
#         else:
#             if (oe==0 and x not in dfa["final_states"]) or (ie ==0 and x not in dfa["final_states"] and x not in dfa["start_states"]):
#                 flag=True
#                 # print(x)
#                 toremove=[]
#                 for y in dfa["transition_function"]:
#                     if x in y:
#                         toremove.append(y)
#                 for i in toremove:
#                     dfa["transition_function"].remove(i)
#                 dfa["states"].remove(x)
#                 if x in dfa["final_states"]:
#                     dfa["final_states"].remove(x)
#     if flag==True:
#         flag=False
#     else:
#         flag=True

# print(dfa)
newletters=set()
for x in range(len(dfa["transition_function"])):
    newletters.add(dfa["transition_function"][x][1])
dfa["letters"]=list(newletters)

def checkDistinguishable(x):
    if x == []: return True
    global mp1,mp2,transition_table,dfa
    mp={}
    for y in range(len(x)):
        mp[x[y]]=[]
        for xt in range(len(dfa["letters"])):
            x1=transition_table[mp2[x[y]]][mp1[dfa["letters"][xt]]]
            for i in range(len(previousp1)):
                if x1 in previousp1[i]:
                    x1=i
                    break
            indx = len(mp[x[y]])
            mp[x[y]].insert(indx,x1)
    
    for key in mp:
        if mp[key]!=mp[x[0]]:
            return False
    return True

def getpartition(x):
    l=2**(len(x))
    leng = l//2
    for i in range(leng):
        s1=[]
        s2=[]
        for j in range(len(x)):
            if i & (2**j):
                indx = len(s1)
                s1.insert(indx,x[j])
            else:
                indx = len(s2)
                s2.insert(indx,x[j])
        
        if checkDistinguishable(s1) :
            if checkDistinguishable(s2):
                return s1,s2
    

def getTransitState(x,y):
    global mp1,previousp1,previousp,mp2,transition_table
    for i in range(len(previousp1)):
        if transition_table[mp2[x]][mp1[y]] in previousp1[i]:
            return previousp[i]

def checkForEqualTransitions(x):
    global transition_table
    global mp2
    mp={}
    for xt in range(len(x)):
        tt=[]
        for r in transition_table[mp2[x[xt]]]:
            if r!='$':
                indx = len(tt)
                tt.insert(indx,'-')
            else:
                indx = len(tt)
                tt.insert(indx,'$')
        exp="".join(tt)
        # print(exp)
        if exp in mp:
            indx = len(mp[exp])
            mp[exp].insert(indx,x[xt])
        else:
            mp[exp]=[x[xt]]
    fs=[]
    for key in mp:
        indx = len(fs)
        fs.insert(indx,mp[key])
    return fs 

start=0
transition_table = [['$' for x in dfa["letters"]] for y in dfa["states"]]
mp1={}
for i in range(len(dfa["letters"])):
    mp1[dfa["letters"][i]]=start
    start+=1
start=0
mp2={}
for i in range(len(dfa["states"])):
    mp2[dfa["states"][i]]=start
    start+=1
for x in range(len(dfa["transition_function"])):
    transition_table[mp2[dfa["transition_function"][x][0]]][mp1[dfa["transition_function"][x][1]]]=mp2[dfa["transition_function"][x][2]]

previousp=[]
p0=[]
startstates=dfa["states"]
for x in range(len(dfa["final_states"])):
    startstates.remove(dfa["final_states"][x])
startstates=checkForEqualTransitions(startstates)
l=checkForEqualTransitions(dfa["final_states"])
p0=startstates
for i in range(len(l)):
    p0.append(l[i])
p=0

previousp=p0
nextstate=[]
while True:
    # print(previousp)
    p+=1
    nextstate.clear()
    previousp1=deepcopy(previousp)
    for x in range(0,len(previousp1)):
        for y in range(0,len(previousp1[x])):
            previousp1[x][y]=mp2[previousp1[x][y]]
            continue
    
    for x in range(0,len(previousp)):
        s1,s2=getpartition(previousp[x])
        # print(s1,s2,"awdwad")
        if s2 == []:
            indx = len(nextstate)
            nextstate.insert(indx,s1)
        elif s1 == []:
            indx = len(nextstate)
            nextstate.insert(indx,s2)
        else:
            indx=len(nextstate)
            nextstate.insert(indx,s1)
            indx=len(nextstate)
            nextstate.insert(indx,s2)
    
    if nextstate == previousp:
        break
    else:
        previousp=deepcopy(nextstate)
        nextstate.clear()

ss=[]
fs=[]
newdfa={}
newdfa['states']=previousp
newdfa['start_states']=[]
newdfa['final_states']=[]
newdfa['letters']=dfa['letters']
newdfa['transition_function'] = []
for i in range(len(dfa['start_states'])):
    for j in range(len(previousp)):
        if (dfa['start_states'][i] in previousp[j]) and (previousp[j] not in ss):
            indx = len(ss)
            ss.insert(indx,previousp[j])
for i in range(len(dfa['final_states'])):
    for j in range(len(previousp)):
        if (dfa['final_states'][i] in previousp[j]) and (previousp[j] not in fs):
            indx = len(fs)
            fs.insert(indx,previousp[j])
for i in range(len(previousp)):
    for j in range(len(dfa['letters'])):
        u=getTransitState(previousp[i][0],dfa['letters'][j])
        if u:
            newdfa["transition_function"].append([previousp[i],dfa['letters'][j],u])

newdfa['start_states']=ss
newdfa['final_states']=fs
g = open(argv[2],"w")
json.dump(newdfa,g,indent=6)