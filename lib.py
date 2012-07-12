import requests
import datetime
import json

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
