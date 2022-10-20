from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json

baseurl = "https://www.fussballdaten.de/regionalliga/west/"
#baseurl = "https://www.fussballdaten.de/regionalliga/nordost/"

path = "/home/ast/fussballdaten/RLW/"
jahr = 2013
spieltagmin = 1
spieltagmax = 38

def ErzeugeFussballdatenJSON(baseurl, jahr, spieltagmin, spieltagmax, path):
#    print(baseurl)
    print("Jahr: " +str(jahr))
    print("Spieltagmin: " +str(spieltagmin))
    print("Spieltagmax: " +str(spieltagmax))
    print()
    baseurl = baseurl +str(jahr) +"/"

    for i in range(spieltagmin, spieltagmax +1):
        url = baseurl +str(i) +"/"
        print(url)

        req = Request(url)
        html_page = urlopen(req)

        soup = BeautifulSoup(html_page, "lxml")

        spieltag = {}
        tabelle = {}
        varSpieltag = 0
        liganame = ""
        datum = ""

        x = soup.find("div", class_="kategorie-headline content")
        x = x.find_all(re.compile("^h[0-9]"))
        x = str(x)
        x = x.split('<br class="visible-xs"/> - ')
        liganame = x[0]
        liganame = liganame.rsplit('>',1)
        liganame = liganame[1]
        varSpieltag = x[1].split('.')
        varSpieltag = varSpieltag[0]
        spieltag["Liga"] = liganame
        spieltag["Spieltag"] = varSpieltag
        tabelle["Liga"] = liganame
        tabelle["Spieltag"] = varSpieltag

        x = soup.find_all(class_="content-spiele")
        x = x[1]

        k = 0
        for i in x:
            j = str(i)
#            print() ##
            if j.find('class="datum-row"') > -1:
                datum = j.split('>')
                datum = datum[1].split('<')
                datum = datum[0]
#                print(datum) ##
            if j.find('class="spiele-row detils"') > -1:
                HeimTeam = j
                HeimTeam = HeimTeam.split('<span class="wappen_icon',1)
                HeimTeam = HeimTeam[0].rsplit('>',1)
                HeimTeam = HeimTeam[1]
                GastTeam = j
                if varSpieltag == "1":
                    GastTeam = GastTeam.split('</a><div class="infos">')
                    GastTeam = GastTeam[0].rsplit('>',1)
                    GastTeam = GastTeam[1]
                else:
                    GastTeam = GastTeam.split('<span class="rang ml10 hidden-xs"')
                    GastTeam = GastTeam[0].rsplit('>',1)
                    GastTeam = GastTeam[1]
                Ergebnis = j
                Ergebnis = Ergebnis.split('</span><span>',1)
                Ergebnis = Ergebnis[0].rsplit('>',1)
                Ergebnis = Ergebnis[1]
                Pause = j
                Pause = Pause.split('</span></a><a href="',1)
                Pause = Pause[0].rsplit('>',1)
                Pause = Pause[1]
#                print(HeimTeam +" " +Ergebnis +" (" +Pause +") " +GastTeam) ##

                spieltag[str(k)] = {}
                spieltag[str(k)]["Heimteam"] = HeimTeam
                spieltag[str(k)]["Gastteam"] = GastTeam
                spieltag[str(k)]["Datum"] = datum
                spieltag[str(k)]["Endergebnis"] = Ergebnis
                spieltag[str(k)]["Pausenergebnis"] = Pause
                k = k +1


        table = soup.find("tbody")


        table["Liga"] = liganame
        table["Spieltag"] = varSpieltag

        i = 0
        for x in table:
            if x == "\n":
                pass
            else:
                tabellenplatz = str(x)
                tabellenplatz = tabellenplatz.split('ranking-number">',1)
                tabellenplatz = tabellenplatz[1].split('<',1)
                tabellenplatz = tabellenplatz[0]

                teamname = str(x)
                teamname = teamname.split('</span> ',1)
                teamname = teamname[1].split('<')
                teamname = teamname[0]

                spiele = str(x)
                spiele = spiele.split('class="text-right">',1)
                spiele = spiele[1].split('<')
                spiele = spiele[0]

                tore = str(x)
                tore = tore.split('class="text-center">',1)
                tore = tore[1].split('<')
                tore = tore[0]

                if(tore == "-:-"):
                    tordiff = tore
                else:
                    tordiff = tore.split(':')
                    tordiff = int(tordiff[0]) - int(tordiff[1])
                    tordiff = str(tordiff)

                punkte = str(x)
                punkte = punkte.split('class="text-right fw600 green">',1)
                punkte = punkte[1].split('<')
                punkte = punkte[0]

                tabelle[str(i)] = {}
                tabelle[str(i)]["Tabellenplatz"] = tabellenplatz
                tabelle[str(i)]["Teamname"] = teamname
                tabelle[str(i)]["Spiel"] = spiele
                tabelle[str(i)]["Tore"] = tore
                tabelle[str(i)]["Tordifferenz"] = tordiff
                tabelle[str(i)]["Punkte"] = punkte


                i = i+1
#                print(tabellenplatz +". " +teamname +" " +spiele + " "+tore +" " +tordiff +" " +punkte) ##

## wird benoetigt um die falsche Array Reihenfolge nachtraeglich zu korrigieren.
#        i = 0
#        for x in spieltag:
#            if(x != "Liga" and x != "Spieltag"):
#                if(int(x) != i):
#                    spieltag[str(i)] = spieltag.pop(x)
#                    i = i +1

## Erzeugt die beiden JSON Dateien
        spieltagpath = path +str(jahr) +"/" +varSpieltag+'_spieltag.json'
        print("saving to file: " +spieltagpath)
        with open(spieltagpath, 'w', encoding='utf-8') as f:
            json.dump(spieltag, f, ensure_ascii=False, indent=4)
        tabellepath = path +str(jahr) +"/" +varSpieltag +'_tabelle.json'
        print("saving to file: " +tabellepath)
        with open(tabellepath, 'w', encoding='utf-8') as f:
            json.dump(tabelle, f, ensure_ascii=False, indent=4)
        print()

#        with open(varSpieltag +'_spieltag.json', 'w', encoding='utf-8') as f:
#            json.dump(spieltag, f, ensure_ascii=False, indent=4)
#        with open(varSpieltag +'_tabelle.json', 'w', encoding='utf-8') as f:
#            json.dump(tabelle, f, ensure_ascii=False, indent=4)

ErzeugeFussballdatenJSON(baseurl, jahr, spieltagmin, spieltagmax, path)


