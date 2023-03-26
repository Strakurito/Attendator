from datetime import datetime
import calendar

class Pracik:
    def __init__(self,jmeno,kchod,premie,platUct,stavby):
        self.jmeno= jmeno
        self.kchod = kchod
        self.premie = premie
        self.platUct = platUct
        self.dochazky = {}
        
        for stavba in stavby:
            self.novaDochazka(stavba)


    def novaDochazka(self, stavba):
        mesic = datetime.now().month
        rok = datetime.now().year
        self.dochazky[stavba] = Dochazka(stavba, mesic, rok)



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
            if calendar.weekday(rok, mesic, den + 1) == 0:
                    self.vikendy.append(den)
            elif calendar.weekday(rok, mesic, den + 1) == 6:
                    self.vikendy.append(den)