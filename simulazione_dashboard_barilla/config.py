import random
from prodotto import Prodotto

def genera_fasi(nome_prodotto, tempo_totale, num_fasi, nomi_fasi):
    #Distribuisce in modo casuale il tempo totale tra le fasi del prodotto
    pesi = [random.uniform(1, 2) for _ in range(num_fasi)]
    somma_pesi = sum(pesi)
    durata_fasi = [(p / somma_pesi) * tempo_totale for p in pesi]
    return dict(zip(nomi_fasi, durata_fasi))

def genera_prodotti():
    #Crea la lista di prodotti vuoti, senza caratteristiche specifiche.
    prodotti = [
        Prodotto("Spaghetti Barilla", None, None, None),
        Prodotto("Frollini Mulino Bianco", None, None, None),
        Prodotto("Pesto Barilla", None, None, None)
    ]
    return prodotti

def genera_quantita(prodotti):
    #Genera quantità casuali di ciascun prodotto da produrre
    return {prodotto.nome: random.randint(500, 2000) for prodotto in prodotti}

def genera_parametri(prodotti):
    #Genera i parametri di produzione per ogni prodotto.
    parametri = {}

    for prodotto in prodotti:
        if prodotto.nome == "Spaghetti Barilla":
            tempo_unitario = round(random.uniform(0.12, 0.14), 3)
            capacita_giornaliera = random.randint(2000, 5000)
            fasi = [
                "Selezione e Macinazione", "Impasto e Gramolatura",
                "Trafilatura", "Essiccazione", "Confezionamento"
            ]
        elif prodotto.nome == "Frollini Mulino Bianco":
            tempo_unitario = round(random.uniform(0.015, 0.017), 3)
            capacita_giornaliera = random.randint(3000, 7000)
            fasi = [
                "Impasto ingredienti", "Formatura biscotti",
                "Cottura", "Raffreddamento e controllo qualità", "Confezionamento"
            ]
        elif prodotto.nome == "Pesto Barilla":
            tempo_unitario = round(random.uniform(0.023, 0.027), 3)
            capacita_giornaliera = random.randint(1000, 3000)
            fasi = [
                "Controllo materie prime", "Pulizia e preparazione",
                "Miscelazione ingredienti", "Pastorizzazione", "Confezionamento"
            ]

        prodotto.tempo_unitario = tempo_unitario
        prodotto.capacita_giornaliera = capacita_giornaliera
        prodotto.fasi = genera_fasi(prodotto.nome, tempo_unitario, len(fasi), fasi)

        parametri[prodotto.nome] = {
            "tempo_unitario": prodotto.tempo_unitario,
            "capacita_giornaliera": prodotto.capacita_giornaliera,
            "fasi": prodotto.fasi
        }

    capacita_complessiva = sum(p.capacita_giornaliera for p in prodotti)
    return parametri, capacita_complessiva
