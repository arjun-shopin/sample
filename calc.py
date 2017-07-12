# calculator
def calc(n):
    
    if n==1:
        a=float(raw_input("Enter number 1 "))
        b=float(raw_input("Enter number 2 "))
        print a+b
    elif n==2:
        a=float(raw_input("Enter number 1 "))
        b=float(raw_input("Enter number 2 "))
        print a-b
    elif n==3:
        a=float(raw_input("Enter number 1 "))
        b=float(raw_input("Enter number 2 "))
        print a*b
    elif n==4:
        a=float(raw_input("Enter number 1 "))
        b=float(raw_input("Enter number 2 "))
        if b==0:
            print "Div Error"
        else:
            print a/b
    elif n==0:
        print "exiting" 
        return None
    else:
        print "Please input appropriate number "
    

n=int(raw_input("Please enter 1 for addition , 2 for subtraction , 3 for multiply and 4 for division , 0 to exit"))
while (n!=0):
    calc(n)
    n=int(raw_input("Please enter 1 for addition , 2 for subtraction , 3 for multiply and 4 for division , 0 to exit"))
    
