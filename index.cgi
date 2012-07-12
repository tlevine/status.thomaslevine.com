#!/usr/bin/env python2
import os
import MySQLdb
import requests
import datetime
import json

# =========================================================
# Settings
# =========================================================

USERNAME = 'status'
PASSWORD = '' 
HOST = 'thomaslevine.db'
DATABASE = 'status'

URLS = [
    'http://thomaslevine.com',
    'http://www.thomaslevine.com',
    'http://git.thomaslevine.com',
    'http://chainsaw.thomaslevine.com',
    'http://hacks.thomaslevine.com',
    'http://couch.thomaslevine.com',
    'http://lorena.co.nz',
    'http://www.lorena.co.nz',
    'http://fadelee.com',
    'http://www.fadelee.com',
    'http://dumptruck.io',
    'http://www.dumptruck.io',
    'http://deadpeoplebornonmybirthday.com',
    'http://www.deadpeoplebornonmybirthday.com',
]

# =========================================================

def __schema(cur):
  cur.execute('''
CREATE TABLE IF NOT EXISTS status (
  url VARCHAR(2000) NOT NULL,
  datetime DATETIME NOT NULL,
  code SMALLINT NOT NULL
);
''')

def __checkurl(url):
    try:
        response = requests.get(url)
    except:
        code = 0
    else:
        code = response.status_code

    return {
        'url': url,
        'code': code,
        'datetime': datetime.datetime.now(),
    }

def get(cur):
    __schema(cur)

    # Get the data
    statuses = []
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
    print json.dumps(statuses)

def post(cur):
    __schema(cur)
    for url in URLS:
        data = __checkurl(url)
        cur.execute('''
INSERT INTO status (url, datetime, code)
VALUES ("%(url)s", "%(datetime)s", "%(code)d")
''' % data)
    cur.commit()

# Connect
db = MySQLdb.connect(
    host=HOST, # your host, usually localhost
    user=USERNAME, # your username
    passwd=PASSWORD, # your password
    db=DATABASE # name of the data base
)
cur = db.cursor() 

print 'Content-type: text/plain'
print ''
if os.environ['REQUEST_METHOD'] == 'GET':
    get(cur)
elif os.environ['REQUEST_METHOD'] == 'POST':
    post(cur)
