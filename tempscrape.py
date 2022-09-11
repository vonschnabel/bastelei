#import time
from influxdb import InfluxDBClient
import requests
import json

from datetime import date, timedelta

client = InfluxDBClient(host='localhost',
        port=8086,
        database='wetter',
        username='admin',
        password='password')

days = []

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2022, 1, 1)
end_date = date(2022, 9, 1)
for single_date in daterange(start_date, end_date):
    days.append(single_date.strftime("%Y-%m-%d"))

#for i in range(0, len(days)):
#    print(days[i])



#dwd_station_id = "01270" # Erfurt Bindersleben
#dwd_station_id = "05424" # Weimar Schöndorf
#dwd_station_id = "02444" # Jena Sternwarte
dwd_station_id = "07368" # Eisenach

#url = "https://api.brightsky.dev/weather?dwd_station_id=01270&date=2022-09-06"
baseurl = "https://api.brightsky.dev/weather?dwd_station_id=" +dwd_station_id + "&date="

for i in range(0, len(days)):
        url = baseurl + days[i]
        print(url)
        r = requests.get(url)
        cont = r.json()
        for j in range(0, 24):
                print(str(cont['weather'][j]['temperature']) + "  " + str(cont['weather'][j]['timestamp']))

                entry = [{
                        "measurement": "Station_" +str(dwd_station_id),
                        "tags": {
                                "Ort": "Eisenach",
                                "dwd_station_id": dwd_station_id
                        },
                        "time": cont['weather'][j]['timestamp'],
                        "fields": {
                                "temperature": cont['weather'][j]['temperature'],
                                "precipitation": cont['weather'][j]['precipitation'],
                                "pressure_msl": cont['weather'][j]['pressure_msl'],
                                "sunshine": cont['weather'][j]['sunshine'],
                                "wind_direction": cont['weather'][j]['wind_direction'],
                                "wind_speed": cont['weather'][j]['wind_speed'],
                                "cloud_cover": cont['weather'][j]['cloud_cover'],
                                "dew_point": cont['weather'][j]['dew_point'],
                                "relative_humidity": cont['weather'][j]['relative_humidity'],
                                "visibility": cont['weather'][j]['visibility'],
                                "wind_gust_direction": cont['weather'][j]['wind_gust_direction'],
                                "wind_gust_speed": cont['weather'][j]['wind_gust_speed'],
                                "condition": cont['weather'][j]['condition'],
                                "icon": cont['weather'][j]['icon']
                        }
                }]
                client.write_points(entry)

        print()
        print()

#r = requests.get(url)
#cont = r.json()
##print(len(cont['weather']))
#for i in range(0, 24):
#    print(str(cont['weather'][i]['temperature']) + "  " + str(cont['weather'][i]['timestamp']))

#print()
#print(cont["AlertsLastMinute"])
#line = 'Alerts,type=assembly AlertsLast24Hours=' +str(cont['AlertsLast24Hours']) +',AlertsLast5Minutes=' +str(cont['AlertsLast5Minutes']) +',AlertsLastHour=' +str(cont['AlertsLastHour']) +',AlertsLastMinute=' +str(cont['AlertsLastMinute'])
#client.write([line], {'db': 'SicherheitstachoAlerts'}, 204, 'line')
#client.close()
#time.sleep(600.0)
