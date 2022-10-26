import string
import time
import urllib.request
from pprint import pprint
import hashlib
import os
import urllib
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
for pagenum in range(22,109):
    print(pagenum)
    try:
        url='http://www.18sexpics.com/galleries/all/date/'+str(pagenum)
        page=requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        all=soup.find_all('div',class_='isotope-item')
        urls=[]
        images_url=[]
        for i in all:
            i1=i.find('a')
            urls.append('https://www.18sexpics.com/'+str(i1.get('href')))
        len(urls)
        for i in urls:
            print(i)
            page=requests.get(i)
            soup = BeautifulSoup(page.text, 'html.parser')
            imgs=soup.find_all('figure',class_='box')
            for j in imgs[3::4]:
                try:
                    src=j.find('a')['href']
                    print(src)
                    save_path = 'data1/'+i.split('/')[-1]+src.split('/')[-1]
                    f = open(save_path,'wb')
                    f.write(requests.get(src).content)
                    f.close()
                except Exception as e:
                    print(e)
                    pass
    except Exception as e:
            print(e)
            pass
 
