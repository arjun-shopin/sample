n=int(raw_input("enter the number of rows"))
for i in range(1,n+1):
    if i <=(n+1)/2 :
        for j in range(1,i+1):
            print "* ",
        print
    else :
        for j in range(i,n+1):
            print "* ",
        print

