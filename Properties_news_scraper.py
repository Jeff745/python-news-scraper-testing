from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.options import Options 
import urllib 
import bs4, requests, smtplib 
import datetime 
from datetime import date 
import numpy 
import openpyxl 
from openpyxl import Workbook 
import pandas as pd 
 
 
options = Options() 
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe' 
driver = webdriver.Firefox(executable_path=r'C:\Users\Lenovo ideapad 1 11\OneDrive\Desktop\SG properties forum\geckodriver.exe', options=options) 
 
driver.get("https://www.edgeprop.sg/property-news") 
sourcecode = driver.page_source 
 
sourcecode=str(sourcecode) 
     
soup = bs4.BeautifulSoup(sourcecode, 'html.parser') 
 
 
links = [] 
linkstext = [] 
for div in soup.find_all(class_='article-container hyperlink'): 
    first_link = next(div.children, None) 
    if first_link is not None: 
        linkstext.append(str(first_link.text)) 
        links.append("https://www.edgeprop.sg" + str(first_link.get('href'))) 
 
 
x = 0 
Repeatedindex =[] 
Uniqueindex = [] 
# no of items in list 
indexno = len(links) 
status = 0 
# first loop 
while (x < indexno): 
  # 2nd loop 
   
  i = x + 1 
  while (i < indexno): 
     if links[x] == links[i]: 
        Repeatedindex.append(i) 
        Repeatedindex.append(x) 
        Uniqueindex.append(x) 
     # i loop 
     i = i+1 
  # x loop 
  x = x + 1 
 
# no of items in repeated index  
Indexrep = len(Repeatedindex) 
y = 0 
while (y < indexno): 
 z = 0 
 status = 0 
 while (z < Indexrep): 
   if y == Repeatedindex[z]: 
     status = 1 
     break 
   # z loop 
   z = z + 1 
 # y loop 
 if status == 0: 
      Uniqueindex.append(y) 
 y = y + 1         
 
o=0 
 
strdate = datetime.datetime.now() 
strdate = strdate.strftime("%d %B %Y") 
strlinks = "News of the Day: " + str(strdate) + "\n\n\n" + "Source: Edgeprop" + "\n\n\n" 
pastposts = [] 
while o < len(Uniqueindex): 
 
  pastposts.append(links[Uniqueindex[o]]) 
 
  o = o + 1 
 
df = pd.read_excel (r'C:/Users/Lenovo ideapad 1 11/OneDrive/Desktop/SG properties forum/data.xlsx', sheet_name='Sheet1') 
 
 
mylist = df.values.tolist() 
 
 
l = 0 
 
while l < len(pastposts): 
    k = 0 
    status = 0 
    while k < len(mylist): 
     j = 0 
     while j < len(mylist[k]): 
      if pastposts[l] == mylist[k][j]: 
        status = 1 
        break 
      j = j + 1 
     k = k + 1 
 
    if status  == 0: 
 
        strlinks = strlinks + linkstext[Uniqueindex[l]] + "\n" + links[Uniqueindex[l]] + "\n\n" 
    l = l + 1 
         
wb = openpyxl.load_workbook('C:/Users/Lenovo ideapad 1 11/OneDrive/Desktop/SG properties forum/data.xlsx') 
ws = wb.active 
ws.append(pastposts) 
 
wb.save('C:/Users/Lenovo ideapad 1 11/OneDrive/Desktop/SG properties forum/data.xlsx') 
 
footer = "Main Chat Group: " + "\n\n" + "https://t.me/SGpropertiesforum" 
 
strlinks = strlinks + footer 
 
if strlinks != "News of the Day: " + str(strdate) + "\n\n\n" + "Source: Edgeprop" + "\n\n\n" + footer : 
 url = "https://api.telegram.org/bot5192130160:AAFHpp3BPD9mrspEgpkFHNGCe0ESNBtx-xc/sendMessage?chat_id=-1001507450706&disable_web_page_preview=true&text={}".format(strlinks) 
 requests.get(url)