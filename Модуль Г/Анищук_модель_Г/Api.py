#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tkinter import *
import webbrowser
import random
from random import randint
from bs4 import BeautifulSoup


# In[ ]:





# In[ ]:





# In[5]:


list_A =['да', 'нет']


# In[6]:


def show_message():
    label["text"] = list_A[randint(0, len(list_A)-1)] # получаем введенный текст
 
root = Tk()
root.title("METANIT.COM")
root.geometry("500x500") 

label = Label(text="Это API может прогнозирования номинации конкурсанта ", justify = CENTER) # создаем текстовую метку
label.pack(anchor=S, fill=X)

label1 = Label(text="Для того чтоб узнать введите ссылку в эту строку ", justify = CENTER) # создаем текстовую метку
label1.pack(anchor=S, fill=X)

entry = Entry(justify = CENTER)
entry.pack(anchor=N, padx=6, pady=6,)
  
btn = Button(text="Click", command=show_message)
btn.pack(anchor=N, padx=6, pady=6)
 
label = Label(text= 'выграет?')
label.pack(anchor=N, padx=6, pady=6)
  
root.mainloop()
    


# In[ ]:




