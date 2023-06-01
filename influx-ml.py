from datetime import datetime, timezone
from influxdb import InfluxDBClient

host = 'localhost'
port = 8086
user = 'telegrafuser'
password = 'Test111'
dbname = 'telegraf'
query = "select time, appname, hostname, severity_code, message from syslog where hostname = 'gateway2' and appname = 'sshd' and message =~ /(?i)opened/;"
client = InfluxDBClient(host, port, user, password, dbname)
result = client.query(query)

sshopened = []
sshclosed = []

for point in result.get_points():
#  print(point)
#  print(point['time'])
  sshopened.append(point['time'])

query = "select time, appname, hostname, severity_code, message from syslog where hostname = 'gateway2' and appname = 'sshd' and message =~ /(?i)closed/;"
result = client.query(query)

for point in result.get_points():
#  print(point)
#  print(point['time'])
  sshclosed.append(point['time'])

print(sshopened)
print()
print(sshclosed)
