import random
from prodotto import Prodotto

def genera_fasi(nome_prodotto, tempo_totale, num_fasi, nomi_fasi):
    """Distribuisce in modo casuale il tempo totale tra le fasi"""
    pesi = [random.uniform(1, 2) for _ in range(num_fasi)]
    somma_pesi = sum(pesi)
    durata_fasi = [(p / somma_pesi) * tempo_totale for p in pesi]
    return dict(zip(nomi_fasi, durata_fasi))


""" Genera i prodotti con i loro parametri e le fasi di produzione.
    Ogni prodotto ha un nome, un tempo unitario di produzione, una capacità giornaliera
    e una lista di fasi di produzione con i relativi tempi.
    I tempi unitari e le capacità giornaliere sono generati casualmente
    all'interno di intervalli specifici.
    Le fasi di produzione sono definite in base al tipo di prodotto.
    I prodotti generati sono:
    - Spaghetti Barilla
    - Frollini Mulino Bianco
    - Pesto Barilla"""
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

""" Genera una quantità casuale di prodotti da produrre
    per ogni prodotto. La quantità è compresa tra 500 e 2000 unità.
    Restituisce un dizionario con il nome del prodotto come chiave
    e la quantità da produrre come valore."""
def genera_quantita(prodotti):
    return {prodotto.nome: random.randint(500, 2000) for prodotto in prodotti}

""" Restituisce un dizionario con i parametri di produzione
    per ogni prodotto, la capacità complessiva di produzione e la lista dei prodotti.
    I parametri includono il tempo unitario,
    la capacità giornaliera e le fasi di produzione."""
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
