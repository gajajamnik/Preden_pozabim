from datetime import *
from datetime import timedelta

import json

class Uporabnik:
    def __init__(self, uporabnisko_ime, geslo, zbirka_predavanj):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.zbirka = zbirka_predavanj

    def v_slovar(self, ime_datoteke):
        return {
            'uporabnisko_ime': self.uporabnisko_ime,
            'geslo': self.geslo,
            'zbirka': self.zbirka.v_slovar()
        }
    
    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def iz_slovarja(cls, slovar):
        uporabnisko_ime = slovar['uporabnisko_ime']
        geslo = slovar['geslo']
        self = cls(uporabnisko_ime, geslo)
        self.zbirka = ZbirkaPredavanj.iz_slovarja(slovar['zbirka'])
        return self

    def preveri_geslo(self, geslo):
        if self.geslo != geslo:
            raise ValueError('Napačno geslo!')


class ZbirkaPredavanj:
    def __init__(self):
        self.predavanja = []
        self.ponavljanja = []

    def v_slovar(self):
        return {
            'predavanja': [predavanje.v_slovar() for predavanje in self.predavanja],
            'ponavljanja': [predavanje.v_slovar() for predavanje in self.ponavljanja]
        }

    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def iz_slovarja(cls, slovar):
        self = cls()
        for predavanje in slovar['predavanja']:
            self.predavanja.append(Predavanje.iz_slovarja(predavanje))
        for ponavljanje in slovar['ponavljanja']:
            self.ponavljanja.append(Predavanje.iz_slovarja(ponavljanje))
        return self

    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar = json.load(datoteka)
        return cls.iz_slovarja(slovar)

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

    #odstrani predavanje iz zbirke
    def odstrani_predavanje(self, predavanje):
        if predavanje in self.predavanja:
            self.predavanja.remove(predavanje)
        elif predavanje in self.ponavljanja:
            self.ponavljanja.remove(predavanje)
        else:
            raise ValueError('Tega predavanja ni v zbirki')


    #ce je datum ustrezen predavanje iz zbirke prestavi doda v ponavljanja
    def dodaj_v_ponavljanja(self):
        danes = date.today()
        changes = False
        vsa_predavanja = self.predavanja
        for predavanje in vsa_predavanja:
            if danes >= predavanje.naslednji_datum:
                if not any(predavanje.v_slovar() == ponavljanje.v_slovar() for ponavljanje in self.ponavljanja):
                    self.ponavljanja.append(predavanje)
                    changes = True
        return changes

    #iz seznama ponavljanja izbere(INDEKS) predavanje, na njem opravi ponovitev in ga odstrani iz seznama ponavljanja
    #funkcija vraca nov datum ponavljanja
    def ponovi_iz_ponavljanja(self, predavanje, uspesnost):
        if 0 <= int(uspesnost) <= 5:
            predavanje.ponovi_predavanje(uspesnost)
            nov_datum = predavanje.naslednji_datum
            self.ponavljanja.remove(predavanje)
            return nov_datum
        else:
            raise ValueError('Uspesnost mora biti podana s stevilko med 0 in 5.')

    

#POMOZNI FUNKCIJI ZA IZRACUN NASLEDNJE PONOVITVE
#izracuna faktor glede na uspesnost
def nov_faktor(uspesnost):
    f = 2.5
    return f + (0.1 - (5 - uspesnost) * (0.08 + (5 - uspesnost) * 0.02))

#izracuna nov interval glede na stari interval, stopnjo in uspesnost
def novi_interval(trenutni_interval, stopnja, uspesnost):
    if stopnja == 0:
        pass
    elif stopnja == 1:
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

    def v_slovar(self):
        return {
            'predmet': self.predmet,
            'tema': self.tema,
            'zadnji_datum': self.zadnji_datum.strftime("%d/%m/%Y"),
            'naslednji_datum': self.naslednji_datum.strftime("%d/%m/%Y"),
            'ponovitve': [{
                'cas_ponovitve': ponovitev.cas_ponovitve.strftime("%d/%m/%Y"),
                'uspesnost': ponovitev.uspesnost,
            } for ponovitev in self.ponovitve],
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        predmet = slovar['predmet']
        tema = slovar['tema']
        self = cls(predmet, tema)
        self.zadnji_datum = datetime.strptime(slovar['zadnji_datum'], "%d/%m/%Y").date()
        self.naslednji_datum = datetime.strptime(slovar['naslednji_datum'], "%d/%m/%Y").date()
        for ponovitev in slovar['ponovitve']:
            self.ponovitve.append(Ponovi.iz_slovarja(ponovitev))
        return self

    #izracuna razliko med zadnjim in novim ponavljanjem (potrebujemo za izracun naslednjega intervala)
    def izracunaj_trenutni_interval(self):
        razlika = self.naslednji_datum - self.zadnji_datum
        razlika_v_dnevih = razlika.days
        return razlika_v_dnevih


    def ponovi_predavanje(self, uspesnost):
        #doda ponovitev v seznam ponovitev
        self.ponovitve.append(Ponovi(uspesnost))
        #izracuna novi interval
        trenutni_interval = self.izracunaj_trenutni_interval()
        stopnja = len(self.ponovitve)
        interval = novi_interval(trenutni_interval, stopnja, uspesnost)
        print(interval)
        #ponovno definiramo zadnji in naslednji datum ponovitve
        datum_dodajanja = date.today()
        dan = datum_dodajanja.day
        mesec = datum_dodajanja.month
        leto = datum_dodajanja.year
        self.zadnji_datum = date(leto, mesec, dan)
        self.naslednji_datum = self.zadnji_datum + timedelta(days=interval)
        

#ob vsaki ponovitvi dodamo uspenost ponovitve po lestvici 0-5
class Ponovi:
    def __init__(self, uspesnost):
        self.cas_ponovitve = date.today()
        self.uspesnost = uspesnost

    @classmethod
    def iz_slovarja(cls, slovar):
        uspesnost = slovar['uspesnost']
        self = cls(uspesnost)
        self.cas_ponovitve = datetime.strptime(slovar['cas_ponovitve'], "%d/%m/%Y")
        return self




zbirka = ZbirkaPredavanj()

zbirka.dodaj_predavanje('analiza', 'vrste')

pred = zbirka.predavanja[0]

pred.zadnji_datum = date(2020, 9, 14)
pred.naslednji_datum = date(2020, 9, 15)

zbirka.dodaj_v_ponavljanja()

zbirka.ponovi_iz_ponavljanja(zbirka.ponavljanja[0], 3)

#pred.izracunaj_trenutni_interval()

#pred.ponovi_predavanje(3)

#pred.ponovi_predavanje(4)