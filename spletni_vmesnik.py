import bottle
from datetime import *
from model import Uporabnik, ZbirkaPredavanj, Predavanje, Ponovi

DATOTEKA_S_STANJEM = 'test.json'

try:
    zbirka = ZbirkaPredavanj.nalozi_stanje(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    zbirka = ZbirkaPredavanj()

@bottle.get('/')
def home():
    zbirka.dodaj_v_ponavljanja()
    return bottle.template('home.html', zbirka=zbirka)

@bottle.post('/dodaj/')
def dodaj():
    predmet = bottle.request.forms['predmet']
    tema = bottle.request.forms['tema']
    zbirka.dodaj_predavanje(predmet, tema)
    bottle.redirect('/')

@bottle.post('/pobrisi/<predmet>/<tema>/')
def pobrisi(predmet, tema):
    zbirka.odstrani_predavanje(predmet, tema)
    bottle.redirect('/')

@bottle.post('/oceni/<predmet>/<tema>/')
def oceni():
    uspesnost = bottle.request.forms['ocena']
    zbirka.ponovi_iz_ponavljanja(predmet, tema, uspesnost)
    bottle.redirect('/')


bottle.run(debug=True, reloader=True)