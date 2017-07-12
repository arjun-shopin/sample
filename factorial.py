# factorial function

def f(n):
    f=1
    for i in range(1,n+1):
        f=f*i
    return f
print(f(4))

def f_w(n):
    f=1
    i=n
    while (i>0):
        f=f*i
        i=i-1
    return f
print (f(4))
    
