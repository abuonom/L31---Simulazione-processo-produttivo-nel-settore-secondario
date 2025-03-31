from flask import Flask, render_template, jsonify
from config import genera_quantita, genera_parametri
from produzione import calcola_tempo_totale

app = Flask(__name__)
prodotti = []

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

    return jsonify({
        "tempo_totale_ore": tempo_totale_ore,
        "tempo_totale_giorni": tempo_totale_giorni,
        "dettagli": dettagli,
        "quantita": quantita
    })

if __name__ == '__main__':
    app.run(debug=True)
