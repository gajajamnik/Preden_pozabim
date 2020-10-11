import bottle
from datetime import *
import random
import os
from model import Uporabnik, ZbirkaPredavanj, Predavanje, Ponovi

zbirke = {}
for ime_datoteke in os.listdir('shranjene_zbirke'):
    st_uporabnika, koncnica = os.path.splitext(ime_datoteke)
    zbirke[st_uporabnika] = ZbirkaPredavanj.nalozi_stanje(os.path.join('shranjene_zbirke', ime_datoteke))

# se ne shranjenemu uporabniku doda novo zbirko, shranjenemu pa vrne svojo zbirko
def zbirka_uporabnika():
    st_uporabnika = bottle.request.get_cookie('st_uporabnika')
    if st_uporabnika is None:
        st_uporabnika = str(random.randint(0, 2 ** 40))
        zbirke[st_uporabnika] = ZbirkaPredavanj()
        bottle.response.set_cookie('st_uporabnika', st_uporabnika, path='/')
    return zbirke[st_uporabnika]

def shrani_zbirko_uporabnika():
    st_uporabnika = bottle.request.get_cookie('st_uporabnika')
    zbirka = zbirke[st_uporabnika]
    zbirka.shrani_stanje(os.path.join('shranjene_zbirke', f'{st_uporabnika}.json'))


@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/preden-pozabim/')

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