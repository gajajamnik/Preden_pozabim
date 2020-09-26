from datetime import date
from model import ZbirkaPredavanj, Predavanje, Ponovi, Uporabnik

# dokler testiram
zbirka = ZbirkaPredavanj()
zbirka.dodaj_predavanje('analiza', 'vrste')
zbirka.dodaj_predavanje('algebra', 'matrike')
zbirka.dodaj_predavanje('algebra', 'determinante')

# umetno nastavimo da je bilo predavanje dodano vceraj
zbirka.predavanja[0].zadnji_datum = date(2020, 9, 20)
zbirka.predavanja[0].naslednji_datum = date(2020, 9, 21)

zbirka.dodaj_v_ponavljanja()

LOGO = '''
  ___            _                              _    _       
 | _ \_ _ ___ __| |___ _ _    _ __  ___ _____ _| |__(_)_ __  
 |  _/ '_/ -_) _` / -_) ' \  | '_ \/ _ \_ / _` | '_ \ | '  \ 
 |_| |_| \___\__,_\___|_||_| | .__/\___/__\__,_|_.__/_|_|_|_|
                             |_|                             
 '''
DATOTEKA_S_STANJEM = 'stanje.json'



# POMOŽNE FUNKCIJE ZA VNOS

def dobro(niz):
    print(f'\033[1;94m{niz}\033[0m')


def slabo(niz):
    print(f'\033[1;91m{niz}\033[0m')

def krepko(niz):
    print(f'\033[1m{niz}\033[0m')

def prikaz_predavanja(predavanje):
    return f'''
    ({predavanje.predmet}, {predavanje.tema}): zadnji datum ponovitve = {predavanje.zadnji_datum}, naslednji datum ponovitve = {predavanje.naslednji_datum}
    '''

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


#SESTAVNI DEL UPORABNIŠKEGA UMESNIKA


def glavni_meni():
    print(LOGO)
    krepko('Pozdravljeni v programu PREDEN POZABIM!')
    print('Za izhod pritisnite Ctrl-C.')
    print
    while True:
        try:
            moznosti = [
                ('dodal predavanje', dodaj_predavanje),
                ('odstranil predavanje', odstrani_predavanje),
                ('pogledal danasnja ponavljanja', danasnja_ponavljanja),
                ('pogledal vsa predavanja', vsa_predavanja),
            ]
            print('Kaj bi rad naredil?')
            izbira = izberi(moznosti)
            print(80 * '=')
            izbira()
            input('Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...')
            print()
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

def odstrani_predavanje():
    print('Katero predavanje želite odstraniti?')
    odstranjeno = izberi([(prikaz_predavanja(predavanje), predavanje) for predavanje in zbirka.predavanja])
    zbirka.odstrani_predavanje(odstranjeno)

def danasnja_ponavljanja():
    if zbirka.ponavljanja == []:
        dobro('Danes nimas nic za ponavljat. Uživaj ;)')
    else:
        print('Katero predavanje želite ponoviti?')
        try:
            ponovljeno = izberi([(prikaz_predavanja(predavanje), predavanje) for predavanje in zbirka.ponavljanja])
            ponovi_predavanje(ponovljeno)
        except ValueError as e:
            slabo(e.args[0])

def ponovi_predavanje(predavanje):
    print('Oceni uspešnost ponovitve od 0 do 5')
    izbira = input('> ')
    uspesnost = int(izbira)
    nov_datum = zbirka.ponovi_iz_ponavljanja(predavanje, uspesnost)
    dobro('Uspešno ste ponovili predavanje. Naslednji datum ponovitve je {}'.format(nov_datum))

def vsa_predavanja():
    if zbirka.predavanja == []:
        print('Zbirka predavanj je prazna.')
        try:
            moznosti = [
                ('dodal predavanje', dodaj_predavanje),
                ('nazaj na osnovni meni', glavni_meni),
            ]
            print('Kaj bi rad naredil?')
            izbira = izberi(moznosti)
            izbira()
        except ValueError as e:
            slabo(e.args[0])
    else:
        for predavanje in zbirka.predavanja:
            print(prikaz_predavanja(predavanje))


glavni_meni()

# to moras obvezno zagnat, da se nalozijo denvna ponavljanja
danasnja_ponavljanja()
