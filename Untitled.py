
# coding: utf-8

# In[68]:

# function to reverse the names of each element in a series
# import pandas as pd 
names = pd.Series([
    'Andre Agassi',
    'Barry Bonds',
    'Christopher Columbus',
    'Daniel Defoe',
    'Emilio Estevez',
    'Fred Flintstone',
    'Greta Garbo',
    'Humbert Humbert',
    'Ivan Ilych',
    'James Joyce',
    'Keira Knightley',
    'Lois Lane',
    'Mike Myers',
    'Nick Nolte',
    'Ozzy Osbourne',
    'Pablo Picasso',
    'Quirinus Quirrell',
    'Rachael Ray',
    'Susan Sarandon',
    'Tina Turner',
    'Ugueth Urbina',
    'Vince Vaughn',
    'Woodrow Wilson',
    'Yoji Yamada',
    'Zinedine Zidane'
])


# In[104]:

# write a code to print only the last names of a 1 D pandas series 
new_names=[]
for i in names:
    new_names.append((i.split()[1]+" "+i.split()[0]))
new_names
# create a function :
def test(a):
    return a.split()[0]+" "+a.split()[1]    
x1=names.apply(test)


# In[131]:

# count the number of spaces in each 
x=pd.Series(['Andre Agassi',
    'Barry Bonds',
    'Christopher  Columbus']
           )
x
unique_array=x.unique()
# function to count the number of spaces 
def count_space(x):
        return x.count(" ")
names.apply(count_space)
# count the number of characters excluding spaces
def count_chars_except_space(x):
    space_count=x.count(" ")
    return len(x)-space_count
names.apply(count_chars_except_space)
    

    


# In[ ]:




# In[ ]:



