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

    # Salva su CSV
    inizializza_csv()
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

    with open(CSV_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        return jsonify(list(reader))


if __name__ == '__main__':
    app.run(debug=True)
