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
        novo_predavanje = Predavanje(predmet, tema)
        self.predavanja.append(novo_predavanje)

    #ce je datum ustrezen predavanje iz zbirke prestavi doda v ponavljanja
    def dodaj_v_ponavljanja(self):
        for predavanje in self.predavanja:
            if date.today >= predavanje.naslednji_datum:
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
        self.zadnji_datum = date.today()  #ob vpisu predavanja se ta datum nastavi na dan vnosa
        self.naslednji_datum = date.today() + timedelta(days=1) #ob vpisu predavanja se to nastavi na en dan po vnosu
        self.ponovitve = []
        self.stopnja = 1
        
    #izracuna razliko med zadnjim in novim ponavljanjem (potrebujemo za izracun naslednjega intervala)
    def izracunaj_trenutni_interval(self):
        razlika = self.naslednji_datum - self.zadnji_datum
        razlika_v_dnevih = razlika.days
        return razlika_v_dnevih


    def ponovi_predavanje(self, uspesnost):
        self.ponovitve.append(Ponovi(uspesnost))
        trenutni_interval = self.izracunaj_trenutni_interval
        

        self.stopnja += 1
        #ob ponovitvi_moramo se spremenit self.zadnji_datum iin self.naslednji_datum
        

    



#ob vsaki ponovitvi dodamo uspenost ponovitve po lestvici 0-5
class Ponovi:
    def __init__(self, uspesnost):
        self.cas_ponovitve = date.today()
        self.uspesnost = uspesnost




#zbirka = ZbirkaPredavanj()

#zbirka.dodaj_predavanje('analiza', 'vrste')