# fibonacci
past=1
present=1
n=int(raw_input("enter till"))
n=n+1
for i in range(1,n):
       future=past+present
       past=present
       present=future
       i=i+1
       print(future)
        
