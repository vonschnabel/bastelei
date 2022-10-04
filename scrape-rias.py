from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

import wget

url = "http://www.rias1.de/werbeschallplatten.html"
path = "/home/ast/rias/werbeschallplatten"

#req = Request("http://www.rias1.de/timeline_nachrichten.htm")
req = Request(url)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
"""
for link in soup.findAll('a'):
#    links.append(link.get('href'))
    var = link.get('href')
    if var is not None:
        if var.find('.mp3') > -1:
#            print("http://www.rias1.de/" +var)
            links.append("http://www.rias1.de/" +var)
        elif var.find('.flac') > -1:
#            print("http://www.rias1.de/" +var)
            links.append("http://www.rias1.de/" +var)
"""
for link in soup.findAll('source'):
#    links.append(link.get('href'))
    var = link.get('src')
    if var is not None:
        if var.find('.mp3') > -1:
#            print("http://www.rias1.de/" +var)
#            print(var)
            links.append("http://www.rias1.de/" +var)
        elif var.find('.flac') > -1:
#            print("http://www.rias1.de/" +var)
#            print(var)
            links.append("http://www.rias1.de/" +var)

faileddownloads = []

print("Number of Found Files: " +str(len(links)))

for i in range(0, len(links)):
    print("Downloading: " +str(i+1) +"/" +str(len(links)) +"  " +links[i])
    try:
        wget.download(links[i], out = path)
    except Exception as exc:
        print(f"wget failed: {str(exc)}")
        faileddownloads.append(links[i])
    print()

print()
print("Number of Failed Downloads: " +str(len(faileddownloads)))
print()
for i in range(0, len(faileddownloads)):
    print(faileddownloads[i])

