from datetime import datetime
import calendar

class Pracik:
    def __init__(self,jmeno,kchod,premie,platUct,stavby):
        self.jmeno= jmeno
        self.kchod = kchod
        self.premie = premie
        self.platUct = platUct
        self.dochazky = {}
        self.srazy = {}
        self.zalohy = [Zaloha(),Zaloha(),Zaloha(),Zaloha(),Zaloha()]
        self.srazy["V"] = 0
        self.srazy["C"] = 0
        self.srazy["P"] = 0
        self.odevy = {}
        self.odevy["T"] = ""
        self.odevy["C"] = 0
        self.odevy["P"] = 0

        for stavba in stavby:
            self.novaDochazka(stavba)


    def novaDochazka(self, stavba):
        mesic = datetime.now().month
        rok = datetime.now().year
        self.dochazky[stavba] = Dochazka(stavba, mesic, rok)

    def srazCelk(self):
        return str(self.srazy["V"] + self.srazy["C"] + self.srazy["P"])

    def hodinyCelk(self):
        total = 0
        for dochazka in self.dochazky.values():
            total += sum(dochazka.dny)
        return str(total)
    def odevyCelk(self):
        return str(self.odevy["C"] * self.odevy["P"])

    def zalohyCelk(self):
        total = 0
        for zaloha in self.zalohy:
            if zaloha.castka == "":
                total += 0
            else:
                total += int(zaloha.castka)
        return str(total)

class Dochazka:
    def __init__(self, stavba, mesic, rok):
        self.mesic= mesic
        self.rok= rok
        self.stavba = stavba
        pocetDni = calendar.monthrange(self.rok,self.mesic)
        self.dny = []
        self.vikendy = []
        for den in range(pocetDni[1]):
            self.dny.append(0)
            if calendar.weekday(rok, mesic, den+1) == 5:
                    self.vikendy.append(den)
            elif calendar.weekday(rok, mesic, den+1) == 6:
                    self.vikendy.append(den)

class Zaloha:
    def __init__(self):
        self.castka = ""
        self.datum = ""

    def newZaloha(self, castka):
        if castka == 0:
            self.datum = " "
        else:
            self.datum = datetime.today().strftime("%d.%m.%Y")
        self.castka = castka