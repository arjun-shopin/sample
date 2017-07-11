result_str="";    
for row in range(0,7):    
   for column in range(0,7):     
       if ((0<row<6 and column == 0) or ((row == 0 or (column<5 and row ==6) or (column>2 and row ==3)) and (column >1 and column < 6))
           or (row == 3 and 1<column <2 and column < 4)or ((0<row<2 or 3<=row<=5)and column==5)):  
           result_str=result_str+"*"    
       else:      
           result_str=result_str+" "    
   result_str=result_str+"\n"    
print(result_str);  
