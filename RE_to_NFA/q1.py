import re 
postfix = "(a+b)"

regex=''.join(postfix)

keys=list(set(re.sub('[^A-Za-z0-9]+', '', regex)+'e'))

s=[];stack=[];start=0;end=1

counter=-1;c1=0;c2=0

for i in regex:
    if i in keys:
        counter=counter+1;c1=counter;counter=counter+1;c2=counter;
        s.append({});s.append({})
        stack.append([c1,c2])
        s[c1][i]=c2
    elif i=='*':
        r1,r2=stack.pop()
        counter=counter+1;c1=counter;counter=counter+1;c2=counter;
        s.append({});s.append({})
        stack.append([c1,c2])
        s[r2]['e']=(r1,c2);s[c1]['e']=(r1,c2)
        if start==r1:start=c1 
        if end==r2:end=c2 
    elif i=='.':
        r11,r12=stack.pop()
        r21,r22=stack.pop()
        stack.append([r21,r12])
        s[r22]['e']=r11
        if start==r11:start=r21 
        if end==r22:end=r12 
    else:
        counter=counter+1;c1=counter;counter=counter+1;c2=counter;
        s.append({});s.append({})
        r11,r12=stack.pop()
        r21,r22=stack.pop()
        stack.append([c1,c2])
        s[c1]['e']=(r21,r11); s[r12]['e']=c2; s[r22]['e']=c2
        if start==r11 or start==r21:start=c1 
        if end==r22 or end==r12:end=c2

print (keys)

print (s)