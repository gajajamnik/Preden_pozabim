#funkcija za izracun naslednjega ponavljanja
#uspesnost se meri po lestvici 0-5 (opis lestvice bo podan na strani/respositoriju)

#funkcija ni dobro definirana problem pri belezenju intervala prejsnjega ponavljanja

def nov_faktor(uspesnost):
    f = 2.5
    return f + (0.1 - (5 - uspesnost) * (0.08 + (5 - uspesnost) * 0.02))


def interval_ponavljanja(stopnja, uspesnost):
    interval = 1
    f = 2.5
    if stopnja == 1:
        pass
    elif stopnja == 2:
        interval = 6
    elif stopnja > 2:
        interval = interval_ponavljanja(stopnja - 1, f) * nov_faktor(uspesnost)
    return interval

#uspesnost ni definirana enako za prejsnje ponavljanje
#treba bo pogledat kasn je biu zadnji interval ponavljanja

#zadnji interval zracunas kot razliko med zadnjim ponavljanjem in novim ponavljanjem