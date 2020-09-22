from datetime import date
from model import ZbirkaPredavanj, Predavanje, Ponovi, Uporabnik

#dokler testiram
zbirka = ZbirkaPredavanj()
zbirka.dodaj_predavanje('analiza', 'vrste')
zbirka.dodaj_predavanje('algebra', 'matrike')
#zbirka.dodaj_predavanje('algebra', 'determinante')

#umetno nastavimo da je bilo predavanje dodano vceraj
zbirka.predavanja[0].zadnji_datum = date(2020, 9, 20)
zbirka.predavanja[0].naslednji_datum = date(2020, 9, 21)

zbirka.dodaj_v_ponavljanja()

#funkcija, ki izbira iz seznama
def izberi(seznam):
    for indeks, element in enumerate(seznam, 1):
        print('{0}) {1}'.format(indeks, element))
        print('{} Ne želim izbrati ničesar'.format(len(seznam) + 1))
    while True:
        izbira = input('> ')
        if 1 <= int(izbira) <= len(seznam) and izbira.isdigit():
            return seznam[int(izbira) - 1]
        elif int(izbira) == len(seznam) + 1 and izbira.isdigit():
            glavni_meni()
        else:
            print('Vnesi število od 1 do {}'.format(len(seznam)))


def glavni_meni():
    while True:
        print('''
        Kaj bi rad naredil?
        1) dodal predavanje
        2) pogledal danasnja ponavljanja
        3) pogledal vsa predavanja
        4) izhod iz programa
        ''')
        izbira = input('> ')
        if izbira == '1':
            dodaj_predavanje()
        elif izbira == '2':
            danasnja_ponavljanja()
        elif izbira == '3':
            vsa_predavanja()
        elif izbira == '4':
            print('Hasta luego')
            break
        else:
            print('Neveljavna izbira')

def dodaj_predavanje():
    predmet = input('Vnesi ime predmeta> ')
    tema = input('Vnesi temo predavanja> ')
    zbirka.dodaj_predavanje(predmet, tema)
    print('Predavanje uspesno dodano')

def danasnja_ponavljanja():
    if zbirka.ponavljanja == []:
        print('Danes nimas nic za ponavljat. Uživaj ;)')
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
            #print('Uspešno ste ponovili predavanje')
        elif int(izbira) == len(seznam) + 1 and izbira.isdigit():
            glavni_meni()
        else:
            print('Vnesi število od 1 do {}'.format(len(seznam)))

def ponovi_predavanje(indeks):
    print('Oceni uspešnost ponovitve od 0 do 5')
    izbira = input('> ')
    uspesnost = int(izbira)
    zbirka.ponovi_iz_ponavljanja(indeks, uspesnost)
    print('Uspešno ste ponovili predavanje')
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

#to moras obvezno zagnat, da se nalozijo denvna ponavljanja
danasnja_ponavljanja()