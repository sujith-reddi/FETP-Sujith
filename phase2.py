st = "pythonprogramming"
l = len(st)
nst = ""
num=16
num=int(num/2)
for i in range(num+1):
    for j in range(num - i):
        print(" ", end='')
    x = (i+(2*i)+1)
    k=((i+(2*i)+1)-l)
    if x>l:
        nst = st[i:i+(2*i)+1] + st[:k]
        if len(nst) < ((2*i)+1):
            prev_str = st[i:i+(2*i)+1]
            ix = ((2*i)+1)-len(prev_str)
            num_repeats = ix // l + 1
            result_string = st * num_repeats
            nst = st[i:i+(2*i)+1] + result_string[:ix]
        print(nst)
    else:
        nst = st[i:k]
        print(st[i:k])
for m in range(num,0,-1):
    for n in range(num+1-m):
        print(" ",end='')
    print(nst[n+1:((2*m) + n)])
