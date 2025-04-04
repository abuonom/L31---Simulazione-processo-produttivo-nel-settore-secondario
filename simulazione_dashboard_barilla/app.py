from flask import Flask, render_template, jsonify, send_file
from config import genera_quantita, genera_parametri
from produzione import calcola_tempo_totale
import csv
import os
import sys
from datetime import datetime

# Gestione delle cartelle per PyInstaller
if getattr(sys, 'frozen', False):
    # Se l'app è stata congelata con PyInstaller
    base_path = sys._MEIPASS
else:
    # Se l'app è eseguita normalmente, usa il percorso corrente
    base_path = os.path.abspath(".")


template_folder = os.path.join(base_path, 'templates')
static_folder = os.path.join(base_path, 'static')

# Crea l'istanza dell'app Flask con cartelle template e static specifiche
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)


prodotti = []
CSV_PATH = os.path.join(base_path, 'storico_produzione.csv')

# Inizializza il file CSV con le intestazioni se non esiste
def inizializza_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Data", "Prodotto", "Quantita", "Tempo Totale (ore)", "Tempo Totale (giorni)"])

# Route principale
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route generazione quantità prodotto randomica
@app.route('/genera-quantita', methods=['GET'])
def genera_quantita_route():
    global prodotti, quantita
    if not prodotti:
        _, _, prodotti = genera_parametri()
    quantita = genera_quantita(prodotti) 
    return jsonify(quantita)

# Route che restituisce i parametri di produzione (tempo unitario, capacità, fasi)
@app.route('/genera-parametri', methods=['GET'])
def genera_parametri_route():
    global prodotti, quantita
    parametri, capacita_complessiva, prodotti = genera_parametri()
    return jsonify({
        "parametri": parametri,
        "capacita_complessiva": capacita_complessiva
    })

# Route che calcola tempo totale di produzione
@app.route('/calcola-tempo', methods=['GET'])
def calcola_tempo_route():
    global prodotti, quantita
    if not prodotti:
        _, _, prodotti = genera_parametri()  # Se i prodotti non sono stati generati, li genera
    if not quantita:  # Verifica se la quantità è già stata generata
        quantita = genera_quantita(prodotti)  # Genera la quantità solo se non è già presente
    tempo_totale_ore, dettagli = calcola_tempo_totale(prodotti, quantita)
    tempo_totale_giorni = round(tempo_totale_ore / 24, 2)  # Conversione tempo in giorni

    inizializza_csv()
    with open(CSV_PATH, mode='a', newline='') as file:
        # Scrittura dei dati sul CSV
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

# Route per lo storico della produzione
@app.route('/storico', methods=['GET'])
def scarica_storico():
    return send_file(CSV_PATH, as_attachment=True)

# Route che restituisce i dati per il grafico della produzione
@app.route('/grafico', methods=['GET'])
def grafico_produzione():
    if not os.path.exists(CSV_PATH):
        return jsonify([])

    cleaned_rows = []
    with open(CSV_PATH, mode='r') as file:
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
    app.run(debug=False)
