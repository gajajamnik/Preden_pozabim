import bottle
from datetime import *
import random
import os
import hashlib
from model import Uporabnik, ZbirkaPredavanj, Predavanje, Ponovi

uporabniki = {}

skrivnost = 'TOP SECRET'

for ime_datoteke in os.listdir('uporabniki'):
    uporabnik = Uporabnik.nalozi_stanje(os.path.join('uporabniki', ime_datoteke))
    uporabniki[uporabnik.uporabnisko_ime] = uporabnik

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=skrivnost)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
    return uporabniki[uporabnisko_ime]

# se ne shranjenemu uporabniku doda novo zbirko, shranjenemu pa vrne svojo zbirko
def zbirka_uporabnika():
    return trenutni_uporabnik().zbirka

def shrani_trenutnega_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.shrani_stanje(os.path.join('uporabniki', f'{uporabnik.uporabnisko_ime}.json'))


@bottle.get('/')
def zacetna_stran():
    shrani_trenutnega_uporabnika()
    bottle.redirect('/preden-pozabim/')

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding='utf-8'))
    zasifrirano_geslo = h.hexdigest()
    if 'nov_racun' in bottle.request.forms and uporabnisko_ime not in uporabniki:
        uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, ZbirkaPredavanj())
        uporabniki[uporabnisko_ime] = uporabnik
    else:
        uporabnik = uporabniki[uporabnisko_ime]
        uporabnik.preveri_geslo(zasifrirano_geslo)
    bottle.response.set_cookie('uporabnisko_ime', uporabnik.uporabnisko_ime, path='/', secret=skrivnost)
    bottle.redirect('/')
  
@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')


@bottle.get('/preden-pozabim/')
def home():
    zbirka = zbirka_uporabnika()
    zbirka.dodaj_v_ponavljanja()  #vsakic posodobi ponovitve glede na dansnji datum
    return bottle.template('home.html', zbirka=zbirka)

@bottle.post('/dodaj/')
def dodaj():
    zbirka = zbirka_uporabnika()
    predmet = bottle.request.forms.getunicode('predmet')
    tema = bottle.request.forms.getunicode('tema')
    zbirka.dodaj_predavanje(predmet, tema)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.post('/pobrisi/<predmet>/<tema>/')
def pobrisi(predmet, tema):
    zbirka = zbirka_uporabnika()
    zbirka.odstrani_predavanje(predmet, tema)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.post('/oceni/<predmet>/<tema>/')
def oceni(predmet, tema):
    zbirka = zbirka_uporabnika()
    uspesnost = bottle.request.forms['ocena']
    zbirka.ponovi_iz_ponavljanja(predmet, tema, uspesnost)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.get('/static/<filename>')
def static_file(filename):
    return bottle.static_file(filename, root='./static')

bottle.run(debug=True, reloader=True)