from datetime import date
from datetime import timedelta

class Uporabnik:
    def __init__(self, uporabnisko_ime, geslo):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo

class ZbirkaPredavanj:
    def __init__(self):
        self.predavanja = []
        self.ponavljanja = []

    #ob vnosu predavanje doda v zbirko
    def dodaj_predavanje(self, predmet, tema):
        datum_dodajanja = date.today()
        dan = datum_dodajanja.day
        mesec = datum_dodajanja.month
        leto = datum_dodajanja.year
        novo_predavanje = Predavanje(predmet, tema)
        #nastavi zadnji in naslednji datum
        novo_predavanje.zadnji_datum = date(leto, mesec, dan)
        novo_predavanje.naslednji_datum = date(leto, mesec, dan) + timedelta(days=1)
        #doda predavanje v zbirko
        self.predavanja.append(novo_predavanje)

    #ce je datum ustrezen predavanje iz zbirke prestavi doda v ponavljanja
    def dodaj_v_ponavljanja(self):
        danes = date.today()
        dan = danes.day
        mesec = danes.month
        leto = danes.year
        for predavanje in self.predavanja:
            if date(leto, mesec, dan) >= predavanje.naslednji_datum:
                self.ponavljanja.append(predavanje)
            else:
                pass

    #iz seznama ponavljanja izbere(INDEKS) predavanje, na njem opravi ponovitev in ga odstrani iz seznama ponavljanja
    def ponovi_iz_ponavljanja(self, indeks_predavanja, uspesnost):
        ponovljeno_predavanje = self.ponavljanja[indeks_predavanja]
        ponovljeno_predavanje.ponovi_predavanje(uspesnost)
        self.ponavljanja.remove(ponovljeno_predavanje)
        #MANJKA BELEZENJE INDEKSA


#izracuna faktor glede na uspesnost
def nov_faktor(uspesnost):
    f = 2.5
    return f + (0.1 - (5 - uspesnost) * (0.08 + (5 - uspesnost) * 0.02))

#izracuna nov interval glede na stari interval, stopnjo in uspesnost
def novi_interval(trenutni_interval, stopnja, uspesnost):
    if stopnja == 1:
        pass
    elif stopnja == 2:
        return 6
    else:
        return trenutni_interval * nov_faktor(uspesnost)


class Predavanje:
    def __init__(self, predmet, tema):
        self.predmet = predmet
        self.tema = tema
        self.zadnji_datum = None  #ob vpisu predavanja se ta datum nastavi na dan vnosa
        self.naslednji_datum = None #ob vpisu predavanja se to nastavi na en dan po vnosu
        self.ponovitve = []
        self.stopnja = len(self.ponovitve) + 1
        
    #izracuna razliko med zadnjim in novim ponavljanjem (potrebujemo za izracun naslednjega intervala)
    def izracunaj_trenutni_interval(self):
        razlika = self.naslednji_datum - self.zadnji_datum
        razlika_v_dnevih = razlika.days
        return razlika_v_dnevih


    def ponovi_predavanje(self, uspesnost):
        #doda ponovitev v seznam ponovitev
        self.ponovitve.append(Ponovi(uspesnost))
        #izracuna novi interval
        trenutni_interval = self.izracunaj_trenutni_interval
        stopnja = self.stopnja
        interval = novi_interval(trenutni_interval, stopnja, uspesnost)
        #ponovno definiramo zadnji in naslednji datum ponovitve
        self.zadnji_datum = self.naslednji_datum
        self.naslednji_datum = self.zadnji_datum + timedelta(days=interval)
        

#ob vsaki ponovitvi dodamo uspenost ponovitve po lestvici 0-5
class Ponovi:
    def __init__(self, uspesnost):
        self.cas_ponovitve = date.today()
        self.uspesnost = uspesnost




#zbirka = ZbirkaPredavanj()

#zbirka.dodaj_predavanje('analiza', 'vrste')