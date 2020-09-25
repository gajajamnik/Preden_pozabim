from datetime import date
from model import ZbirkaPredavanj, Predavanje, Ponovi, Uporabnik

# dokler testiram
zbirka = ZbirkaPredavanj()
zbirka.dodaj_predavanje('analiza', 'vrste')
zbirka.dodaj_predavanje('algebra', 'matrike')
# zbirka.dodaj_predavanje('algebra', 'determinante')

# umetno nastavimo da je bilo predavanje dodano vceraj
zbirka.predavanja[0].zadnji_datum = date(2020, 9, 20)
zbirka.predavanja[0].naslednji_datum = date(2020, 9, 21)

zbirka.dodaj_v_ponavljanja()

# POMOŽNE FUNKCIJE ZA VNOS


def dobro(niz):
    print(f'\033[1;94m{niz}\033[0m')


def slabo(niz):
    print(f'\033[1;91m{niz}\033[0m')

def krepko(niz):
    print(f'\033[1m{niz}\033[0m')


def vnesi_stevilo(pozdrav):
    while True:
        try:
            stevilo = input(pozdrav)
            return int(stevilo)
        except ValueError:
            slabo('Prosim, da vneste število')


# funkcija, ki izbira iz seznama
def izberi(seznam):
    for indeks, (oznaka, _) in enumerate(seznam, 1):
            print(f'{indeks}) {oznaka}')
    while True:
        izbira = vnesi_stevilo('> ')
        if 1 <= izbira <= len(seznam):
            _, element = seznam[izbira - 1]
            return element
        else:
            slabo(f'Izberi število med 1 in {len(seznam)}')


def glavni_meni():
    krepko('Pozdravljeni v programu PREDEN POZABIM!')
    print('Za izhod pritisnite Ctrl-C.')
    print
    while True:
        try:
            moznosti = [
                ('dodal predavanje', dodaj_predavanje),
                ('pogledal danasnja ponavljanja', danasnja_ponavljanja),
                ('pogledal vsa predavanja', vsa_predavanja),
            ]
            print('Kaj bi rad naredil?')
            izbira = izberi(moznosti)
            print(80 * '=')
            izbira()
        except ValueError as e:
            slabo(e.args[0])
        except KeyboardInterrupt:
            print()
            print('Nasvidenje!')
            return


def dodaj_predavanje():
    predmet = input('Vnesi ime predmeta> ')
    tema = input('Vnesi temo predavanja> ')
    zbirka.dodaj_predavanje(predmet, tema)
    dobro('Predavanje uspesno dodano')

def danasnja_ponavljanja():
    if zbirka.ponavljanja == []:
        dobro('Danes nimas nic za ponavljat. Uživaj ;)')
    else:
        izberi_ponavljanje()

def izberi_ponavljanje():
    seznam = zbirka.ponavljanja
    print('Katero predavanje želite ponoviti?')
    for indeks, predavanje in enumerate(seznam, 1):
        predmet = predavanje.predmet
        tema = predavanje.tema
        zadnji_datum = predavanje.zadnji_datum
        naslednji_datum = predavanje.naslednji_datum
        print('''
        {0}) predmet: {1}, tema: {2}, zadnji datum ponavljanja: {3}, naslednji datum ponavljanja: {4}
        '''.format(indeks, predmet, tema, zadnji_datum, naslednji_datum))
        print('''
        {}) Ne želim ponoviti ničesar
        '''.format(len(seznam) + 1))
    while True:
        izbira = input('> ')
        if 1 <= int(izbira) <= len(seznam) and izbira.isdigit():
            indeks = int(izbira) - 1
            ponovi_predavanje(indeks)
            # print('Uspešno ste ponovili predavanje')
        elif int(izbira) == len(seznam) + 1 and izbira.isdigit():
            glavni_meni()
        else:
            print('Vnesi število od 1 do {}'.format(len(seznam)))

def ponovi_predavanje(indeks):
    print('Oceni uspešnost ponovitve od 0 do 5')
    izbira = input('> ')
    uspesnost = int(izbira)
    nov_datum = zbirka.ponovi_iz_ponavljanja(indeks, uspesnost)
    dobro('Uspešno ste ponovili predavanje. Naslednji datum ponovitve je {}'.format(nov_datum))
    glavni_meni()

def vsa_predavanja():
    for predavanje in zbirka.predavanja:
        predmet = predavanje.predmet
        tema = predavanje.tema
        zadnji_datum = predavanje.zadnji_datum
        naslednji_datum = predavanje.naslednji_datum
        print('''
        predmet: {0}
        tema: {1}
        zadnji datum ponavljanja: {2}
        naslednji datum ponavljanja: {3}
        '''.format(predmet, tema, zadnji_datum, naslednji_datum))


glavni_meni()

# to moras obvezno zagnat, da se nalozijo denvna ponavljanja
danasnja_ponavljanja()
