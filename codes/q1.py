import json
import numpy as np 
import sys

states=0

def checkformat(y):
	if (y<48 or y>57) and (y<97 or y>122) and (y<65 or y>90):
		return False
	return True

def get_pre(ch):
	if ch in ['+']:
		return 1
	if ch in ['*']:
		return 2
	if ch in ['.']:
		return 3
	if ch in ['(']:
		return 4

def shunt(x):
	stack=[]
	outstring=""
	for i in x:
		ch=i
		if checkformat(ord(ch)):
			outstring=outstring+ch
		elif ch == '(':
			stack.insert(len(stack),ch)
		elif ch == ')':
			while len(stack)>0 and stack[len(stack)-1]!='(':
				outstring=outstring+stack[len(stack)-1]
				stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
		else:
			while len(stack)>0 and get_pre(ch)>=get_pre(stack[len(stack)-1]):
				outstring=outstring+stack[len(stack)-1]
				stack.pop(len(stack)-1)
			stack.insert(len(stack),ch)
	while len(stack)>0:
		outstring=outstring+stack[len(stack)-1]
		stack.pop(len(stack)-1)
	return outstring

def pars_str(x):
	res=[]
	for i in range(len(x)-1):
		res.insert(len(res),x[i])
		if checkformat(ord(x[i])) and checkformat(ord(x[i+1])):
			res.insert(len(res),'.')
		elif x[i]==')' and x[i+1] == '(':
			res.insert(len(res),'.')
		elif checkformat(ord(x[i+1])) and x[i]==')':
			res.insert(len(res),'.')
		elif x[i+1]=='(' and checkformat(ord(x[i])):
			res.insert(len(res),'.')
		elif x[i] == '*' and (checkformat(ord(x[i+1]) or x[i+1] == '(')):
			res.insert(len(res),'.')
	check = x[len(x)-1]
	if( check != res[len(res)-1]):
		res += check
	return ''.join(res)

def NFA_sym(ch):
	global letters
	letters.update(set({ch}))
	global states
	val = ["Q{}".format(states),ch,"Q{}".format(states+1)]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	states=states+2
	ret = list(["Q{}".format(states-2),"Q{}".format(states-1)])
	return ret

def nfa_unio(nfa1,nfa2):
	global states
	val = ["Q{}".format(states),'$',nfa1[0]]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	val = ["Q{}".format(states),'$',nfa2[0]]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	val = [nfa1[1],'$',"Q{}".format(states+1)]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	val = [nfa2[1],'$',"Q{}".format(states+1)]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	states=states+2
	return ["Q{}".format(states-2),"Q{}".format(states-1)]

def loop(nfa1):
	global states
	val = [nfa1[1],'$',nfa1[0]]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	val = ["Q{}".format(states),'$',nfa1[0]]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	val = [nfa1[1],'$',"Q{}".format(states+1)]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	val = ["Q{}".format(states),'$',"Q{}".format(states+1)]
	nfa["transition_function"].insert(len(nfa["transition_function"]),val)
	states=states+2
	return ["Q{}".format(states-2),"Q{}".format(states-1)]

def concatenation(nfa1,nfa2):
	global states
	indx = len(nfa['transition_function'])
	val = [nfa1[1],'$',nfa2[0]]
	nfa['transition_function'].insert(indx,val)
	return [nfa1[0],nfa2[1]]	

def re2nfa(x):
	stack=list([])
	xt=""
	for i in x:
		if checkformat(ord(i)):
			stack.insert(len(stack),NFA_sym(i))
		elif i == '+':
			xt=nfa_unio(stack[len(stack)-2],stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
		elif i == "*":
			xt=loop(stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
		else:
			xt=concatenation(stack[len(stack)-2],stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
	nfa["start_states"]=[xt[0]]
	nfa["final_states"]=[xt[1]]

letters=set({})

f = open(sys.argv[1],"r")
x=json.load(f)
nfa={}
nfa["states"]=[]
nfa["letters"]=[]
nfa["transition_function"]=[]
x=x["regex"]
x=pars_str(x)
x=shunt(x)
re2nfa(x)

s=set({})
for x in range(len(nfa["transition_function"])):
	s.update(set({nfa["transition_function"][x][0]}))
	s.update(set({nfa["transition_function"][x][2]}))

templis = list(letters)
nfa["letters"]=templis
s=list(s)
s.sort(key=lambda a:int(a[1:]))
nfa["states"]=s

g = open(sys.argv[2],'w')
json.dump(nfa,g,indent=6)