from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import pandas as pd




client = InfluxDBClient(host='localhost',
                        port=8086,
                        username='tank_user',
                        password='Test111',
                        database='tankstellen')

##client.query('SELECT "duration" FROM "pyexample"."autogen"."brushEvents" WHERE time > now() - 4d GROUP BY "user"')

data = client.query('select Spritpreis_Super from spritpreise where ID = 24764 limit 20')
#data = client.query('select Spritpreis_Super from spritpreise where ID = 24764 order by time desc')
#data = client.query('select Spritpreis_Super from spritpreise where ID = 24764 order by time desc limit 400')
client.close()
data = list(data)

for x in data[0]:
  print(x['time'])
  tmp = x['time'].split('.')
  zeit = datetime.fromisoformat(tmp[0])
  zeit += timedelta(hours=1)
  print(zeit.isoweekday(),zeit.hour,zeit.minute)
  print()
