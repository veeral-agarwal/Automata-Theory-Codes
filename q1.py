import json
import numpy as np 
import sys

states=0

def isLetterOrDigit(y):
	if (y<48 or y>57) and (y<97 or y>122) and (y<65 or y>90):
		return False
	return True

def getPrecedence(ch):
	if ch in ['+']:
		return 1
	if ch in ['*']:
		return 2
	if ch in ['.']:
		return 3
	if ch in ['(']:
		return 4

def shuntingyard(x):
	stack=[]
	outstring=""
	for i in x:
		print(outstring)
		ch=i
		if isLetterOrDigit(ord(ch)):
			outstring=outstring+ch
		elif ch == '(':
			stack.insert(len(stack),ch)
		elif ch == ')':
			while len(stack)>0 and stack[len(stack)-1]!='(':
				outstring=outstring+stack[len(stack)-1]
				stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
		else:
			while len(stack)>0 and getPrecedence(ch)>=getPrecedence(stack[len(stack)-1]):
				outstring=outstring+stack[len(stack)-1]
				stack.pop(len(stack)-1)
			stack.insert(len(stack),ch)
	while len(stack)>0:
		outstring=outstring+stack[len(stack)-1]
		stack.pop(len(stack)-1)
	return outstring

def parseString(x):
	res=[]
	for i in range(len(x)-1):
		res.insert(len(res),x[i])
		if isLetterOrDigit(ord(x[i])) and isLetterOrDigit(ord(x[i+1])):
			res.insert(len(res),'.')
		elif x[i]==')' and x[i+1] == '(':
			res.insert(len(res),'.')
		elif isLetterOrDigit(ord(x[i+1])) and x[i]==')':
			res.insert(len(res),'.')
		elif x[i+1]=='(' and isLetterOrDigit(ord(x[i])):
			res.insert(len(res),'.')
		elif x[i] == '*' and (isLetterOrDigit(ord(x[i+1]) or x[i+1] == '(')):
			res.insert(len(res),'.')
	if( x[len(x)-1] != res[len(res)-1]):
		res += x[len(x)-1]
	return ''.join(res)

def symbolNFA(ch):
	global letters
	letters.update(set({ch}))
	global states
	# print("fffff")
	nfa["transition_function"].insert(len(nfa["transition_function"]),["Q{}".format(states),ch,"Q{}".format(states+1)])
	states=states+2
	return ["Q{}".format(states-2),"Q{}".format(states-1)]

def unionNFA(nfa1,nfa2):
	global states
	nfa["transition_function"].insert(len(nfa["transition_function"]),["Q{}".format(states),'$',nfa1[0]])
	nfa["transition_function"].insert(len(nfa["transition_function"]),["Q{}".format(states),'$',nfa2[0]])
	nfa["transition_function"].insert(len(nfa["transition_function"]),[nfa1[1],'$',"Q{}".format(states+1)])
	nfa["transition_function"].insert(len(nfa["transition_function"]),[nfa2[1],'$',"Q{}".format(states+1)])
	states=states+2
	return ["Q{}".format(states-2),"Q{}".format(states-1)]

def loopNFA(nfa1):
	print(nfa1)
	global states
	nfa["transition_function"].insert(len(nfa["transition_function"]),[nfa1[1],'$',nfa1[0]])
	nfa["transition_function"].insert(len(nfa["transition_function"]),["Q{}".format(states),'$',nfa1[0]])
	nfa["transition_function"].insert(len(nfa["transition_function"]),[nfa1[1],'$',"Q{}".format(states+1)])
	nfa["transition_function"].insert(len(nfa["transition_function"]),["Q{}".format(states),'$',"Q{}".format(states+1)])
	states=states+2
	return ["Q{}".format(states-2),"Q{}".format(states-1)]

def concatNFA(nfa1,nfa2):
	global states
	indx=0
	for x in range(len(nfa["transition_function"])):
		# print(nfa1,x)
		if nfa1[1] == nfa["transition_function"][x][2]:
			nfa["transition_function"][indx][2]=nfa2[0]
		indx=indx+1
	return [nfa1[0],nfa2[1]]	

def regexToNFA(x):
	stack=list([])
	xt=""
	for i in x:
		if isLetterOrDigit(ord(i)):
			stack.insert(len(stack),symbolNFA(i))
		elif i == '+':
			xt=unionNFA(stack[len(stack)-2],stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
		elif i == "*":
			xt=loopNFA(stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
		else:
			xt=concatNFA(stack[len(stack)-2],stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
	nfa["start_states"]=xt[0]
	nfa["final_states"]=xt[1]

letters=set({})

f = open('./regtc.json')
x=json.load(f)
nfa={}
nfa["states"]=[]
nfa["letters"]=[]
nfa["transition_function"]=[]
x=x["regex"]
x=parseString(x)
print(x)
x=shuntingyard(x)
regexToNFA(x)
print(nfa["transition_function"])
s=set({})
for x in range(len(nfa["transition_function"])):
	s.update(set({nfa["transition_function"][x][0]}))
	s.update(set({nfa["transition_function"][x][2]}))

templis = list(letters)
nfa["letters"]=templis
s=list(s)
s.sort(key=lambda a:int(a[1:]))
nfa["states"]=s
print(nfa)
g = open('./outna.json','w')
json.dump(nfa,g)