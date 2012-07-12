#!/usr/bin/env python2
import os
import MySQLdb
from lib import get, post
from settings import USERNAME, PASSWORD, HOST, DATABASE, URLS

# Connect
db = MySQLdb.connect(
    host=HOST, # your host, usually localhost
    user=USERNAME, # your username
    passwd=PASSWORD, # your password
    db=DATABASE # name of the data base
)
cur = db.cursor() 

if os.environ['REQUEST_METHOD'] == 'GET':
    get(cur)
elif os.environ['REQUEST_METHOD'] == 'POST':
    post(cur)
