n=int(input("Enter row:"))
result_str="";    
for row in range(0,n):    
   for column in range(0,n):     
       if (column == 1 or ((row == 0 or row == n-1) and (column > 1 and column < n-1)) or (row == n/2 and column > 1 and column < n-2)):  
           result_str=result_str+"*"    
       else:      
           result_str=result_str+" "    
   result_str=result_str+"\n"    
print(result_str);
