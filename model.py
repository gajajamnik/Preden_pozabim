import datetime

class Uporabnik:
    def __init__(self, uporabnisko_ime, geslo):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo

class ZbirkaPredavanj:
    def __init__(self, predavanja):
        self.predavanja = []

    def dodaj_predavanje(self, predmet, tema):
        self.predavanja.append(Predavanje(predmet, tema))

class Predavanje:
    def __init__(self, predmet, tema):
        self.predmet = predmet
        self.tema = tema
        self.zadnji_datum = None  #na zacetku moras to nastavit da bo datum ko dodas predavanje
        self.naslednji_datum = None
        
        #to je datum ki ga bomo zracunali s funkcijo interval
        self.ponovitve = []
        self.stopnja = 1
        #dodaj atribut za belezenje zadnjega intervala(to rabis za izracun naslednjega intervala)
        #self.zadnji_interval = self.naslednji_datum - self.zadnji_datum

    def ponovi_predavanje(self, uspesnost):
        self.ponovitve.append(Ponovi(uspesnost))
        self.stopnja += 1
        self.zadnji_datum = Ponovi(uspesnost).cas_ponovitve

    #def izracun_novega_datuma(self, uspesnost, zadnji_datum):



#ob vsaki ponovitvi dodamo uspenost ponovitve po lestvici 0-5
class Ponovi:
    def __init__(self, uspesnost):
        self.cas_ponovitve = datetime.date.today()
        self.uspesnost = uspesnost


#prvo_predavanje = Predavanje('analiza', 'vrste')




