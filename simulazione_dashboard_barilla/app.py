from flask import Flask, render_template, jsonify, send_file
from config import genera_quantita, genera_parametri
from produzione import calcola_tempo_totale
import csv
import os
from datetime import datetime

app = Flask(__name__)
prodotti = []
CSV_PATH = 'storico_produzione.csv'

# Inizializza il file CSV con intestazioni se non esiste
def inizializza_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Data", "Prodotto", "Quantita", "Tempo Totale (ore)", "Tempo Totale (giorni)"])

""" Sequenza di route per il dashboard
    - /: dashboard principale
    - /genera-quantita: genera una quantità casuale di prodotti da produrre
    - /genera-parametri: genera i parametri di produzione
    - /calcola-tempo: calcola il tempo totale di produzione
    - /storico: scarica lo storico della produzione in CSV
    - /grafico: restituisce i dati per il grafico della produzione"""
    
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/genera-quantita', methods=['GET'])
def genera_quantita_route():
    global prodotti
    if not prodotti:
        _, _, prodotti = genera_parametri()
    quantita = genera_quantita(prodotti)
    return jsonify(quantita)

@app.route('/genera-parametri', methods=['GET'])
def genera_parametri_route():
    global prodotti
    parametri, capacita_complessiva, prodotti = genera_parametri()
    return jsonify({
        "parametri": parametri,
        "capacita_complessiva": capacita_complessiva
    })

@app.route('/calcola-tempo', methods=['GET'])
def calcola_tempo_route():
    global prodotti
    if not prodotti:
        _, _, prodotti = genera_parametri()
    quantita = genera_quantita(prodotti)
    tempo_totale_ore, dettagli = calcola_tempo_totale(prodotti, quantita)
    tempo_totale_giorni = round(tempo_totale_ore / 24, 2)

    inizializza_csv()
    #Scrive i dati calcolati nel CSV 
    with open(CSV_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        for prodotto in prodotti:
            qta = quantita[prodotto.nome]
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d"),
                prodotto.nome,
                qta,
                round(prodotto.tempo_unitario * qta, 2),
                round((prodotto.tempo_unitario * qta) / 24, 2)
            ])

    return jsonify({
        "tempo_totale_ore": tempo_totale_ore,
        "tempo_totale_giorni": tempo_totale_giorni,
        "dettagli": dettagli,
        "quantita": quantita
    })

@app.route('/storico', methods=['GET'])
def scarica_storico():
    return send_file(CSV_PATH, as_attachment=True)

@app.route('/grafico', methods=['GET'])
def grafico_produzione():
    if not os.path.exists(CSV_PATH):
        return jsonify([])

    cleaned_rows = []
    with open(CSV_PATH, mode='r') as file:
        # Legge il CSV e filtra le righe vuote
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("Data") and row.get("Prodotto") and row.get("Quantita"):
                try:
                    float(row["Quantita"])
                    cleaned_rows.append(row)
                except ValueError:
                    pass

    return jsonify(cleaned_rows)



if __name__ == '__main__':
    app.run(debug=True)
