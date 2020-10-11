import bottle
from datetime import *
import random
import os
from model import Uporabnik, ZbirkaPredavanj, Predavanje, Ponovi

uporabniki = {
    'gaja': Uporabnik('gaja', '123', ZbirkaPredavanj())
}

zbirke = {}
for ime_datoteke in os.listdir('shranjene_zbirke'):
    uporabnisko_ime, koncnica = os.path.splitext(ime_datoteke)
    zbirke[uporabnisko_ime] = ZbirkaPredavanj.nalozi_stanje(os.path.join('shranjene_zbirke', ime_datoteke))

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime')
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
    return uporabniki[uporabnisko_ime]

# se ne shranjenemu uporabniku doda novo zbirko, shranjenemu pa vrne svojo zbirko
def zbirka_uporabnika():
    return trenutni_uporabnik().zbirka

def shrani_zbirko_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.zbirka.shrani_stanje(os.path.join('shranjene_zbirke', f'{uporabnisko_ime}.json'))


@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/preden-pozabim/')

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms['uporabnisko_ime']
    geslo = bottle.request.forms['geslo']
    uporabnik = uporabniki[uporabnisko_ime]
    uporabnik.preveri_geslo(geslo)
    bottle.response.set_cookie('uporabnisko_ime', uporabnisko_ime, path='/')

@bottle.get('/preden-pozabim/')
def home():
    zbirka = zbirka_uporabnika()
    zbirka.dodaj_v_ponavljanja()
    return bottle.template('home.html', zbirka=zbirka)

@bottle.post('/dodaj/')
def dodaj():
    zbirka = zbirka_uporabnika()
    predmet = bottle.request.forms.getunicode('predmet')
    tema = bottle.request.forms.getunicode('tema')
    zbirka.dodaj_predavanje(predmet, tema)
    shrani_zbirko_uporabnika()
    bottle.redirect('/')

@bottle.post('/pobrisi/<predmet>/<tema>/')
def pobrisi(predmet, tema):
    zbirka = zbirka_uporabnika()
    zbirka.odstrani_predavanje(predmet, tema)
    shrani_zbirko_uporabnika()
    bottle.redirect('/')

@bottle.post('/oceni/<predmet>/<tema>/')
def oceni(predmet, tema):
    zbirka = zbirka_uporabnika()
    uspesnost = bottle.request.forms['ocena']
    zbirka.ponovi_iz_ponavljanja(predmet, tema, uspesnost)
    shrani_zbirko_uporabnika()
    bottle.redirect('/')


bottle.run(debug=True, reloader=True)