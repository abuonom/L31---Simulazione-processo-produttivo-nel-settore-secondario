def calcola_tempo_totale(prodotti, quantita):
    #Calcola il tempo totale di produzione di tutti i prodotti e restituisce i dettagli delle fasi
    tempo_totale = 0
    dettagli_tempo = {}

    for prodotto in prodotti:
        qta = quantita[prodotto.nome]  
        tempo_prodotto = prodotto.tempo_unitario * qta  

        fasi_singole = {}
        fasi_totali = {}

        for fase, durata in prodotto.fasi.items():
            fasi_singole[fase] = round(durata, 5)  
            fasi_totali[fase] = round(durata * qta, 2)

        dettagli_tempo[prodotto.nome] = {
            "tempo_totale_prodotto": round(tempo_prodotto, 2),
            "fasi_singole": fasi_singole,
            "fasi_totali": fasi_totali
        }

        tempo_totale += tempo_prodotto  # Somma il tempo di produzione per ogni prodotto

    return round(tempo_totale, 2), dettagli_tempo
