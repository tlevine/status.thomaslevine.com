#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Relevant characters: ⚠⚛☭⚙
import os
import MySQLdb
import urllib2
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
    'http://status.thomaslevine.com',
]

# =========================================================

def put(cur):
  cur.execute('''
CREATE TABLE status (
  url VARCHAR(2000) NOT NULL,
  datetime DATETIME NOT NULL,
  code SMALLINT NOT NULL
);
''')
  cur.execute('CREATE INDEX IF NOT EXISTS status_url ON `status` (url)')
  cur.execute('CREATE INDEX IF NOT EXISTS status_datetime ON `status` (datetime)')
  cur.execute('CREATE INDEX IF NOT EXISTS status_code ON `status` (code)')

def __checkurl(url):
    try:
        response = urllib2.urlopen(url)
    except:
        code = 0
    else:
        code = response.code

    return {
        'url': url,
        'code': code,
        'datetime': datetime.datetime.now(),
    }

def get(cur):
    # Get the data
    statuses = []
    cur.execute("SELECT distinct url from status")
    for row in cur.fetchall():
        statuses.append({'url': row[0]})

    for status in statuses:
        cur.execute('''
SELECT `code` from `status`
WHERE `url` = "%s"
ORDER BY `datetime` DESC
LIMIT 1
''' % status['url'])
        status['code'] = cur.fetchall()[0][0]
    print json.dumps(statuses)

def post(cur):
    for url in URLS:
        print url
        data = __checkurl(url)
        cur.execute('''
INSERT INTO status (url, datetime, code)
VALUES ("%(url)s", "%(datetime)s", "%(code)d")
''' % data)

# Connect
db = MySQLdb.connect(
    host=HOST, # your host, usually localhost
    user=USERNAME, # your username
    passwd=PASSWORD, # your password
    db=DATABASE # name of the data base
)
cur = db.cursor() 

if os.environ.get('REQUEST_METHOD', None) == 'GET':
    print 'Content-type: application/json'
    print ''
    get(cur)
elif os.environ.get('REQUEST_METHOD', None) == 'PUT':
    put(cur)
else:
    print 'Content-type: text/plain'
    print ''
    post(cur)
    db.commit()
