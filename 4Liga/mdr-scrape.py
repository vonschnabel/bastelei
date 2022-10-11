from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json
#import wget

#url = "https://www.mdr.de/sport/ergebnisse/fussball-zweite-bundesliga-104.html"
#url = "https://www.mdr.de/sport/ergebnisse/fussball-dritte-liga-108.html"
#url = "https://www.mdr.de/sport/ergebnisse/fussball-regionalliga-nordost-104.html"
#url = "https://www.mdr.de/sport/ergebnisse/fussball-nofv-oberliga-sued-104.html"
#url = "https://www.mdr.de/sport/ergebnisse/fussball-thueringenliga-102.html"

url = "https://www.mdr.de/sport/ergebnisse/fussball-regionalliga-nordost-achtter-spieltag-102.html"
req = Request(url)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

spieltag = {}
tabelle = {}
varSpieltag = 0

for x in soup.find_all("h3", class_="headline"):
    var = str(x)
    if var.find('Spieltag') > -1:
        varSpieltag = var.split('<h3 class="headline">')
        varSpieltag = varSpieltag[1]
        varSpieltag = varSpieltag.split('.')
        varSpieltag = varSpieltag[0]
        spieltag["Spieltag"] = varSpieltag

#print(varSpieltag +". Spieltag")
#print()

HeimTeam = ""
GastTeam = ""
j = 0

for x in soup.findAll("div", class_="match"):
    y = x.select('td[class*="heim tid"]') # Name Heim Verein
    z = x.select('td[class*="gast tid"]') # Name Gast Verein
    u = x.select('td[class*="ende"]') # Endergebnis
    v = x.select('td[class*="pause"]') # Pausen Ergebnis
    for i in range(0, len(y)):
        varheim = str(y[i])
        HeimTeam = varheim.split('>')
        HeimTeam = HeimTeam[1]
        HeimTeam = HeimTeam.split('<')
        HeimTeam = HeimTeam[0]

        vargast = str(z[i])
        GastTeam = vargast.split('>')
        GastTeam = GastTeam[1]
        GastTeam = GastTeam.split('<')
        GastTeam = GastTeam[0]

        varergebnis = str(u[i])
        varergebnis = varergebnis.strip()
        Ergebnis = varergebnis.split('\n')
        Ergebnis = Ergebnis[1]
        Ergebnis = Ergebnis.split('\n')
        Ergebnis = Ergebnis[0]

        if(Ergebnis != "0:0"):
            varpause = str(v[i])
            varpause = varpause.strip()
            Pause = varpause.split('\n')
            Pause = Pause[1]
            Pause = Pause.split('\n')
            Pause = Pause[0]
        else:
            Pause = "(" +Ergebnis +")"

        spieltag[str(j)] = {}
        spieltag[str(j)]["Heimteam"] = HeimTeam
        spieltag[str(j)]["Gastteam"] = GastTeam
        spieltag[str(j)]["Endergebnis"] = Ergebnis
        spieltag[str(j)]["Pausenergebnis"] = Pause
        j = j+1

#        print(HeimTeam + " " +Ergebnis +" " +Pause +" " +GastTeam)
#    print()

table = soup.find("table", class_="datentabelle tabelle")
zeile = table.select('tr[class*="zeile"]')
j = 0

for x in range(0, len(zeile)):
    teamnametable = str(zeile[x].select('th[class*="mannschaft"]'))
    teamnametable = teamnametable.split('title="Zum Saisonspielplan">')
    teamnametable = teamnametable[1]
    teamnametable = teamnametable.split('<')
    teamnametable = teamnametable[0]

    platz = str(zeile[x].select('td[class*="platz"]'))
    platz = platz.split('>')
    platz = platz[1]
    platz = platz.split('\n')
    platz = platz[1]
    platz = platz.split('<')
    platz = platz[0]

    spiele = str(zeile[x].select('td[class*="spiele"]'))
    spiele = spiele.split('>')
    spiele = spiele[1]
    spiele = spiele.split('\n')
    spiele = spiele[1]
    spiele = spiele.split('<')
    spiele = spiele[0]

    gewonnen = str(zeile[x].select('td[class*="gewonnen"]'))
    gewonnen = gewonnen.split('>')
    gewonnen = gewonnen[1]
    gewonnen = gewonnen.split('\n')
    gewonnen = gewonnen[1]
    gewonnen = gewonnen.split('<')
    gewonnen = gewonnen[0]

    unentschieden = str(zeile[x].select('td[class*="unentschieden"]'))
    unentschieden = unentschieden.split('>')
    unentschieden = unentschieden[1]
    unentschieden = unentschieden.split('\n')
    unentschieden = unentschieden[1]
    unentschieden = unentschieden.split('<')
    unentschieden = unentschieden[0]

    verloren = str(zeile[x].select('td[class*="verloren"]'))
    verloren = verloren.split('>')
    verloren = verloren[1]
    verloren = verloren.split('\n')
    verloren = verloren[1]
    verloren = verloren.split('<')
    verloren = verloren[0]

    tore = str(zeile[x].select('td[class*="tore"]'))
    tore = tore.split('>')
    tore = tore[1]
    tore = tore.split('\n')
    tore = tore[1]
    tore = tore.split('<')
    tore = tore[0]

    diff = str(zeile[x].select('td[class*="diff"]'))
    diff = diff.split('>')
    diff = diff[1]
    diff = diff.split('\n')
    diff = diff[1]
    diff = diff.split('<')
    diff = diff[0]

    punkte = str(zeile[x].select('td[class*="punkte"]'))
    punkte = punkte.split('>')
    punkte = punkte[1]
    punkte = punkte.split('\n')
    punkte = punkte[1]
    punkte = punkte.split('<')
    punkte = punkte[0]

    tabelle[str(j)] = {}
    tabelle[str(j)]["Teamname"] = teamnametable
    tabelle[str(j)]["Platz"] = platz
    tabelle[str(j)]["Spiele"] = spiele
    tabelle[str(j)]["Gewonnen"] = gewonnen
    tabelle[str(j)]["Unentschieden"] = unentschieden
    tabelle[str(j)]["Verloren"] = verloren
    tabelle[str(j)]["Tore"] = tore
    tabelle[str(j)]["Tordifferenz"] = diff
    tabelle[str(j)]["Punkte"] = punkte

    j = j+1

#    print(platz + ". " +teamnametable + " " +spiele + " " +gewonnen + " " +unentschieden +" " +verloren +" " +tore +" " +diff +" " +punkte)

#print(spieltag)
#print()
#print(tabelle)
#spieltagjson = json.dumps(spieltag, indent = 4)
#tabellejson = json.dumps(tabelle, indent = 4)
#print()
#print(spieltagjson)
#print()
#print(tabellejson)

with open(varSpieltag +'_spieltag.json', 'w', encoding='utf-8') as f:
    json.dump(spieltag, f, ensure_ascii=False, indent=4)

with open(varSpieltag +'_tabelle.json', 'w', encoding='utf-8') as f:
    json.dump(tabelle, f, ensure_ascii=False, indent=4)
