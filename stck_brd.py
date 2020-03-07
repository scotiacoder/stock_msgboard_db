# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 10:14:41 2018

@author: toshiba
"""

import string
import time #time.sleep(seconds)
import datetime
import csv
import re
import random
from bs4 import BeautifulSoup
import requests

http = requests.session()
#where i left off: i need to somehow append the updated_Pids
#at the BEGINNING of the text file


def load_file(text_file):#string
  l = []
  in_file = open(text_file, 'r')
  txt = in_file.read()
  count=0
  in_file.close()
  regex = r"[0-9]{8}"
  matches = re.findall(regex, txt)	
  for match in matches:
    l.append(match)
    count+=1
  print("current pid count:", str(count))
  l = list(set(l))
  l.sort(key=int, reverse=True)
  return l

def update_pids():
  post_id =[]
  old = load_file('pids.txt')
  pid_found = False
  
  #find most recent pid in list 'a'
  stop = old[0]
  print("Updating pids until", str(old[0]), "is found")
  i = 1
  rqsts = 0
  #pull pids from page 1 and stop when reach most recent pid in 'a'

  while pid_found == False:
    url = 'http://www.stockhouse.com/companies/bullboard?symbol=t.weed&page=' + str(i)
    time.sleep(random.randint(1,2))
    cookies = dict(BCPermissionLevel='PERSONAL')
    page = http.get(url, headers={"User-Agent": "Mozilla/5.0"}, cookies=cookies) #new
    rqsts += 1
    i += 1
    print("Requests sent:",rqsts)
    soupy = BeautifulSoup(page.text, features='lxml')
    bull_content = soupy.find('div', {'class':'bullboard-content'})   
    
    for link in bull_content.find_all('a', {'class':''}, href=True):
      if 'postid=' in link['href']: 
        p_id = link['href'].split('postid=')[1]
        if str(p_id) != stop:
          post_id.append(p_id)
        else:
          pid_found = True
          
  post_id = list(set(post_id))
  post_id.extend(old)
  post_id.sort(key=int, reverse=True)
  print("Output file of post id: pids.txt")
  file_name = 'pids.txt'     
  f1 = open(file_name, 'w')
  post_id = list(set(post_id))
  post_id.sort(key=int, reverse=True)#sort newest first
  f1.write(str(post_id)) 
  f1.close()
  
  return True #list(set(post_id))

def clean(s):
  tmp = ''
  for char in s:
    if char in string.printable:
      tmp += char
  return tmp

#######below is code to get info from individual postid
  
def collect_data(post_ids): #takes list of post ids, gets data, write to csv
  with open('pid_data2.csv', 'w') as myfile:
    wr = csv.writer(myfile, delimiter=',', quoting=csv.QUOTE_ALL)
    for i in range(0, len(post_ids)):
      time.sleep(random.randint(1,2))   
      url = 'http://www.stockhouse.com/companies/bullboard/t.weed/?postid='
      url += str(post_ids[i])
      print("Grabbing post_id:", str(post_ids[i]))
      data = []#[postid,access date, username, postdate, number of reads,
      #subject line, comment]   
      cell1 = post_ids[i]#postid
      now = datetime.datetime.now()
      cell2 = now.strftime("%m-%d-%Y %H:%M")#accessed on
      response = http.get(url)
      soup = BeautifulSoup(response.text, features='lxml')
      if soup.find("div", {"class": "post-content"}):       
        post_user = soup.find("a", {"class":"PostUser"})
        cell3 = post_user['title']#adds username
        post_date = soup.find("div",{"class":"post-detail-info col-md-5"}).text
        post_date = post_date.strip()   
        cell4 = post_date[:post_date.index('\r\n')]#date
        cell5 = post_date[post_date.index('\n')+2:post_date.index('R')].strip()#adds readnumber   
        post_subj = soup.find("h3").text.strip()
        cell6 = clean(post_subj)
        post_content = (soup.find("div", {"class": "post-content"}).text).strip()
        cell7 = clean(post_content)
        #add the text comment
        #data=[id, accessed_on, username, post_date, post_reads, subj_line, comment_text]
        data = [cell1, cell2, cell3, cell4, cell5, cell6, cell7]
        wr.writerow(data)
      else:
        wr.writerow([cell1,cell2,'comment_removed'])
        
    myfile.close()
  return "CSV file has been created!"

update_pids()

#f = open('pids.txt', 'r')
#temp_list = f.read()
#f.close()
#regex = r"[0-9]{8}"
#matches = re.findall(regex, temp_list)
#compiled_pids = []
#
#for match in matches:
#  compiled_pids.append(match)
#
#
#collect_data(compiled_pids)