n=int(raw_input("enter the number between 1500 and 2700"))
if n >=1500 and n<=2700:
    if n %7==0 :
        if n%5==0:
            print"divisible by 7 and 5"
        else:
            print"not divisible by 5 but divisible by 7"
    elif n%5==0:
        if n%7 ==0:
            print" divisible by 7 and 5"
        else:
            print"not divisible by 7 but divisible by 5"
            
    else:
            print "not divisible by 7 and 5"
else :
    print "please enter only between 1500 and 2700" 
