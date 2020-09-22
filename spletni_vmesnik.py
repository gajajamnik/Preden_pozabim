import bottle
from datetime import date
from model import Uporabnik, ZbirkaPredavanj, Predavanje, Ponovi

#treba je definirat zbirko predavanj za vsakega uporabnika posebej
# zbirka_predavanj = Uporabnik.zbirka_predavanj()

zbirka = ZbirkaPredavanj()
zbirka.dodaj_predavanje('analiza', 'vrste')

@bottle.get('/')
def osnovna_stran():
    return bottle.template('osnovna_stran.tpl')


bottle.run(debug=True, reloader=True)