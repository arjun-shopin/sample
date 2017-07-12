# fibonacci
past=1
present=1
n=int(raw_input("enter till"))
i=n
while(i>0):
       future=past+present
       past=present
       present=future
       i=i-1
       print(future)
        
