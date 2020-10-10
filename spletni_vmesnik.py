import bottle
from datetime import *
from model import Uporabnik, ZbirkaPredavanj, Predavanje, Ponovi

DATOTEKA_S_STANJEM = 'test.json'

try:
    zbirka = ZbirkaPredavanj.nalozi_stanje(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    zbirka = ZbirkaPredavanj()

@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/preden-pozabim/')

@bottle.get('/preden-pozabim/')
def home():
    zbirka.dodaj_v_ponavljanja()
    return bottle.template('home.html', zbirka=zbirka)

@bottle.post('/dodaj/')
def dodaj():
    predmet = bottle.request.forms.getunicode('predmet')
    tema = bottle.request.forms.getunicode('tema')
    zbirka.dodaj_predavanje(predmet, tema)
    zbirka.shrani_stanje(DATOTEKA_S_STANJEM)
    bottle.redirect('/')

@bottle.post('/pobrisi/<predmet>/<tema>/')
def pobrisi(predmet, tema):
    zbirka.odstrani_predavanje(predmet, tema)
    zbirka.shrani_stanje(DATOTEKA_S_STANJEM)
    bottle.redirect('/')

@bottle.post('/oceni/<predmet>/<tema>/')
def oceni(predmet, tema):
    uspesnost = bottle.request.forms['ocena']
    zbirka.ponovi_iz_ponavljanja(predmet, tema, uspesnost)
    zbirka.shrani_stanje(DATOTEKA_S_STANJEM)
    bottle.redirect('/')


bottle.run(debug=True, reloader=True)