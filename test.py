from model import Uporabnik, ZbirkaPredavanj, Predavanje, Ponovi

from datetime import date

zbirka = ZbirkaPredavanj()

zbirka.dodaj_predavanje('analiza', 'vrste')

zbirka.dodaj_predavanje('algebra', 'matrike')

#umetno nastavim zadnji datum na vcerajsnji in naslednji datum na danasnji

pred2 = zbirka.predavanja[1]
pred2.zadnji_datum = date(2020, 9, 14)
pred2.naslednji_datum = date(2020, 9, 15)

zbirka.dodaj_v_ponavljanja()

#preverjeno, za ustrezen datum funkcija doda predavanje na seznam ponavljanja