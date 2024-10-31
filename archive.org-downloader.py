from bs4 import BeautifulSoup
import requests
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import os.path

numberofparalleldownloads = 4
ContinueDownload = True
forbiddenstrings = ["'","/","\"","|"]
typestodownload = [".mp4"]
url = "https://archive.org/download/eine_schrecklich_nette_familie/Eine%20schrec                                                                   klich%20nette%20Familie/"
path = "/home/ast/Eine schrecklich nette Familie"

# Links von der Webseite sammeln
def getlinksfromwebsite(url, typestodownload):
  r = requests.get(url)
  soup = BeautifulSoup(r.content, "html.parser")
  links = []
  webpage = soup.find_all('a')
  if webpage:
    for entry in webpage:
      if entry.has_attr('href'):
        for type in typestodownload:
          if entry['href'].lower().find(type) != -1 and entry['href'].find("ia.m                                                                   p4") == -1:
            links.append([url + "/" + entry['href'], entry.contents[0]])
  return links

links = getlinksfromwebsite(url, typestodownload)

def download_url(url):
  chunk_size = 1024
  filename = url[1]
  for string in forbiddenstrings:
    filename = filename.replace(string, "")
  file_path = os.path.join(path, filename)
  url = url[0]

  # Abrufen der Dateiinfos
  headers = {}
  r = requests.get(url, stream=True)
  total = int(r.headers.get('content-length', 0))
  r.close()

  # Falls Datei existiert, abgleichen und Download ggf. fortsetzen
  if os.path.isfile(file_path):
    downloaded_size = os.path.getsize(file_path)
    #print(filename,"downloaded_size:",downloaded_size,"total:",total)
    if downloaded_size < total and ContinueDownload == True:
      headers['Range'] = f'bytes={downloaded_size}-'
      print(f"Download fortsetzen: {filename} ab Byte {downloaded_size} / {total                                                                   }")
    elif downloaded_size == total:
      print(f"{filename} bereits vollständig heruntergeladen.")
      return filename
    else:
      print(f"{filename} ist größer als die Quelle und wird übersprungen.")
      return filename
  else:
    downloaded_size = 0

  # Datei herunterladen
  with requests.get(url, headers=headers, stream=True) as r, open(file_path, 'ab                                                                   ') as file, tqdm(
    desc=filename,
    total=total,
    initial=downloaded_size,
    unit='iB',
    unit_scale=True,
    unit_divisor=1024,
  ) as bar:
    for data in r.iter_content(chunk_size=chunk_size):
      size = file.write(data)
      bar.update(size)
  return filename

# Paralleles Herunterladen mit mehreren Threads
results = ThreadPool(numberofparalleldownloads).imap_unordered(download_url, lin                                                                   ks)
for r in results:
  print(r)
