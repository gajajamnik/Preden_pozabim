from datetime import *
from datetime import timedelta

import json

class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, zbirka_predavanj):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.zbirka = zbirka_predavanj

    def v_slovar(self):
        return {
            'uporabnisko_ime': self.uporabnisko_ime,
            'zasifrirano_geslo': self.zasifrirano_geslo,
            'zbirka': self.zbirka.v_slovar()
        }
    
    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)


    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_stanja = json.load(datoteka)
            uporabnisko_ime = slovar_stanja['uporabnisko_ime']
            zasifrirano_geslo = slovar_stanja['zasifrirano_geslo']
            zbirka = ZbirkaPredavanj.iz_slovarja(slovar_stanja['zbirka'])
            return cls(uporabnisko_ime, zasifrirano_geslo, zbirka)

    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            raise ValueError('Napačno geslo!')
        else:
            return True


class ZbirkaPredavanj:
    def __init__(self):
        self.predavanja = []

    def v_slovar(self):
        return {
            'predavanja': [predavanje.v_slovar() for predavanje in self.predavanja],
        }

    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def iz_slovarja(cls, slovar):
        self = cls()
        for predavanje in slovar['predavanja']:
            self.predavanja.append(Predavanje.iz_slovarja(predavanje))
        return self

    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar = json.load(datoteka)
        return cls.iz_slovarja(slovar)

    #ob vnosu predavanje doda v zbirko
    def dodaj_predavanje(self, predmet, tema):
        datum_dodajanja = date.today()
        #shranimo podatke o datumu dodajanja v spremenljivke
        dan = datum_dodajanja.day
        mesec = datum_dodajanja.month
        leto = datum_dodajanja.year
        novo_predavanje = Predavanje(predmet, tema)
        #nastavi zadnji in naslednji datum(prvi interval med datumoma bo vedno 1)
        novo_predavanje.zadnji_datum = date(leto, mesec, dan)
        novo_predavanje.naslednji_datum = date(leto, mesec, dan) + timedelta(days=1)
        #doda predavanje v zbirko in preveri da predavanja z takim imenom(kombinacija predmeta in teme) še ni v zbirki
        for predavanje in self.predavanja:
            if predavanje.predmet == predmet and predavanje.tema == tema:
                raise ValueError('Predavanje s takim imenom že obstaja!')
        self.predavanja.append(novo_predavanje)

    #odstrani predavanje iz zbirke
    def odstrani_predavanje(self, predmet, tema):
        for i, pred in enumerate(self.predavanja):
            if pred.predmet == predmet and pred.tema == tema:
                predavanje_indeks = i
        del self.predavanja[predavanje_indeks]
        
    #ce je datum ustrezen spremeni atribut ponovi za predavanje iz zbirke
    def dodaj_v_ponavljanja(self):
        danes = date.today()
        vsa_predavanja = self.predavanja
        for predavanje in vsa_predavanja:
            if danes >= predavanje.naslednji_datum:
                predavanje.ponovi = True   #atribut za ponavljanje nastavis na True
        

    #glede na izbrano kombinacijo predmet, tema(kombinacija je enolicna) poisce ustrezno predavanje in na njem opravi ponovitev(na podlagi sprejete uspesnosti)
    #funkcija vraca nov datum ponavljanja
    def ponovi_iz_ponavljanja(self, predmet, tema, uspesnost):
        for pred in self.predavanja:
            if pred.predmet == predmet and pred.tema == tema:
                #preveris da je vnesena uspesnost ustrezna
                if 0 <= int(uspesnost) <= 5:
                    pred.ponovi_predavanje(uspesnost)
                    nov_datum = pred.naslednji_datum
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
        self.ponovi = False 
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
        #doda ponovitev v seznam ponovitev predavanja
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
        #atribut ponovi nastavi ponovno na False
        self.ponovi = False
        

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
