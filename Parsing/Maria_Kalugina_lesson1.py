#!/usr/bin/env python
# coding: utf-8

# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
# 

# In[1]:


#pip install requests


# In[2]:


import requests
from pprint import pprint
import json


# In[3]:


# Имя пользователя github
username = "mariakalugina"


# In[5]:


#https://api.github.com/users/username/repos?sort=updated&direction=desc&visibility=all
url = f'https://api.github.com/users/{username}/repos'


# In[6]:


params = {'sort':'updated',
          'direction':'desc',
          'visibility':'all'
         }


# In[7]:


# делаем запрос и возвращаем json
user_data = requests.get(url,params).json()


# довольно распечатать данные JSON
pprint(user_data)


# In[19]:


for rep_name in user_data:
  pprint(rep_name['name'])


# In[8]:


out_file = open('json_out','w+')
json.dump(user_data,out_file)


# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# In[31]:



url_vk = 'https://api.vk.com/method/groups.get'
params_vk = {'v':'5.52',
             'extended':'1',
             'access_token':#место для токена
# делаем запрос и возвращаем json
user_data_vk = requests.get(url_vk,params_vk)
if user_data_vk.ok:
    user_data_vk = user_data_vk.json()
    for gr in user_data_vk.get('response').get("items"):
       print (gr.get("name"))


# довольно распечатать данные JSON
#pprint(user_data_vk)
    


# In[32]:


out_file2 = open('json_out','w+')
json.dump(user_data_vk,out_file2)


# In[ ]:




