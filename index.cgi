#!/usr/bin/env python2
import MySQLdb
from settings import USERNAME, PASSWORD, HOST, DATABASE

# Connect
db = MySQLdb.connect(
    host=HOST, # your host, usually localhost
    user=USERNAME, # your username
    passwd=PASSWORD, # your password
    db=DATABASE # name of the data base
)
cur = db.cursor() 

