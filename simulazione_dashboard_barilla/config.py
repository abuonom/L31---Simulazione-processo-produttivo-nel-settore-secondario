import random
from prodotto import Prodotto

def genera_prodotti():
    return [
        Prodotto("Spaghetti Barilla", 0.13, random.randint(2000, 5000), {
            "Selezione e Macinazione": 0.02,
            "Impasto e Gramolatura": 0.02,
            "Trafilatura": 0.03,
            "Essiccazione": 0.05,
            "Confezionamento": 0.01
        }),
        Prodotto("Frollini Mulino Bianco", 0.016, random.randint(3000, 7000), {
            "Impasto ingredienti": 0.004,
            "Formatura biscotti": 0.004,
            "Cottura": 0.004,
            "Raffreddamento e controllo qualità": 0.002,
            "Confezionamento": 0.002
        }),
        Prodotto("Pesto Barilla", 0.025, random.randint(1000, 3000), {
            "Controllo materie prime": 0.005,
            "Pulizia e preparazione": 0.005,
            "Miscelazione ingredienti": 0.005,
            "Pastorizzazione": 0.005,
            "Confezionamento": 0.005
        })
    ]

def genera_quantita(prodotti):
    return {prodotto.nome: random.randint(500, 2000) for prodotto in prodotti}

def genera_parametri():
    prodotti = genera_prodotti()
    parametri = {
        p.nome: {
            "tempo_unitario": p.tempo_unitario,
            "capacita_giornaliera": p.capacita_giornaliera,
            "fasi": p.fasi
        } for p in prodotti
    }
    capacita_complessiva = sum(p.capacita_giornaliera for p in prodotti)
    return parametri, capacita_complessiva, prodotti
