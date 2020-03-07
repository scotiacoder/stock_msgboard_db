# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 08:25:19 2018

@author: toshiba
"""
from __future__ import print_function
import mysql.connector
import getpass
import csv
csv.field_size_limit(100000000)

DB_NAME = 'stockhouse'
config = {
  'user': 'root',
  'password': getpass.getpass('Enter password: '),
  'host': '127.0.0.1',
  'database': DB_NAME,
  'raise_on_warnings': True,
}

TABLES = {}
TABLES['stock'] = (
    "CREATE TABLE `stock` ("
    "  `stock_id` int(9) NOT NULL,"
    "  `pull_date` varchar(50) NOT NULL,"
    "  `user_name` varchar(100) ," 
    "  `post_date` varchar(50) ,"
    "  `views` int(4) ,"
    "  `subject` varchar(100),"
    "  `content` longblob,"
    "  PRIMARY KEY (`stock_id`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(**config)
mycursor = cnx.cursor()

#mycursor.execute(TABLES['stock'])
c = open('pid_data2.csv', 'r', newline='')
data = csv.reader(c, delimiter=',')

sql = "INSERT INTO stock (stock_id, pull_date, user_name, post_date, views, subject, content) VALUES (%s, %s, %s, %s, %s, %s, %s)"

for row in data:
  if row != []:
    max_field = len(row)
    if max_field == 7:
      val = (int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
      mycursor.execute(sql, val)
      cnx.commit()
    else:
      val = (int(row[0]), row[1], "none","none",'0',"none","none")
      mycursor.execute(sql, val)
      cnx.commit()
      
cnx.close()
