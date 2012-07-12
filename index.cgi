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

def __schema():
  cur.execute('''
CREATE TABLE IF NOT EXISTS status (
  url VARCHAR(2000) NOT NULL,
  datetime DATETIME NOT NULL,
  code SMALLINT NOT NULL
);
''')

def get():
    statuses = []

    # Get the data
    cur.execute("SELECT distinct url from status")
    for row in cur.fetchall():
        statuses.append({'url': row[0]})

    for status in statuses:
        status['code'] = cur.execute('''
SELECT code from status
WHERE url = "%s"
ORDER BY datetime DESC
LIMIT 1
''')

def post():
    pass
