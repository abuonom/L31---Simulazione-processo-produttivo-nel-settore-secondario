import random
from prodotto import Prodotto

def genera_fasi(nome_prodotto, tempo_totale, num_fasi, nomi_fasi):
    """Distribuisce in modo casuale il tempo totale tra le fasi"""
    pesi = [random.uniform(1, 2) for _ in range(num_fasi)]
    somma_pesi = sum(pesi)
    durata_fasi = [(p / somma_pesi) * tempo_totale for p in pesi]
    return dict(zip(nomi_fasi, durata_fasi))

def genera_prodotti():
    prodotti = []

    # Spaghetti Barilla
    tempo_unitario_sb = round(random.uniform(0.12, 0.14), 3)
    capacita_sb = random.randint(2000, 5000)
    fasi_sb = [
        "Selezione e Macinazione", "Impasto e Gramolatura",
        "Trafilatura", "Essiccazione", "Confezionamento"
    ]
    prodotti.append(Prodotto("Spaghetti Barilla", tempo_unitario_sb, capacita_sb,
                             genera_fasi("Spaghetti", tempo_unitario_sb, len(fasi_sb), fasi_sb)))

    # Frollini Mulino Bianco
    tempo_unitario_fr = round(random.uniform(0.015, 0.017), 3)
    capacita_fr = random.randint(3000, 7000)
    fasi_fr = [
        "Impasto ingredienti", "Formatura biscotti",
        "Cottura", "Raffreddamento e controllo qualità", "Confezionamento"
    ]
    prodotti.append(Prodotto("Frollini Mulino Bianco", tempo_unitario_fr, capacita_fr,
                             genera_fasi("Frollini", tempo_unitario_fr, len(fasi_fr), fasi_fr)))

    # Pesto Barilla
    tempo_unitario_pb = round(random.uniform(0.023, 0.027), 3)
    capacita_pb = random.randint(1000, 3000)
    fasi_pb = [
        "Controllo materie prime", "Pulizia e preparazione",
        "Miscelazione ingredienti", "Pastorizzazione", "Confezionamento"
    ]
    prodotti.append(Prodotto("Pesto Barilla", tempo_unitario_pb, capacita_pb,
                             genera_fasi("Pesto", tempo_unitario_pb, len(fasi_pb), fasi_pb)))

    return prodotti

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
