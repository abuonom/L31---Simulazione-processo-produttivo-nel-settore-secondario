# Progetto Simulazione Processo Produttivo

## Requisiti

- **Python 3.x** installato sulla tua macchina.
- **Flask** per il server web.

---

## Come avviare il progetto

### 1. **Modalità classica (server web Flask)**

#### Passaggi:

1. **Installa le dipendenze**:
   Prima di eseguire l'app, è necessario installare le dipendenze. Puoi farlo con il comando pip:

   ```bash
   pip install -r requirements.txt
   ```

2. **Esegui il server Flask**:
   Nella cartella principale del progetto, esegui il seguente comando:

   ```bash
   python app.py
   ```

   Questo avvierà un server Flask in modalità sviluppo. Puoi accedere all'applicazione nel tuo browser all'indirizzo:

   ```
   http://127.0.0.1:5000
   ```

   Qui potrai interagire con la dashboard, generare quantità e parametri casuali, calcolare il tempo di produzione e visualizzare lo storico.

---

### 2. **Modalità eseguibile**

Se desideri avviare l'applicazione senza dover configurare Python ogni volta, puoi utilizzare l'eseguibile standalone.
Una volta avviato, puoi accedere all'applicazione tramite il browser, come nella modalità classica:

   ```
   http://127.0.0.1:5000
   ```

---

## Funzionalità dell'applicazione

L'applicazione consente di:

- **Generare Quantità**: genera una quantità casuale di unità per ciascun prodotto.
- **Generare Parametri di Produzione**: fornisce i parametri di produzione per ogni prodotto, come il tempo unitario e la capacità giornaliera.
- **Calcolare il Tempo di Produzione**: calcola il tempo totale necessario per produrre tutti i prodotti.
- **Scaricare lo Storico**: consente di scaricare un file CSV contenente lo storico delle produzioni.
- **Visualizzare un Grafico della Produzione**: mostra un grafico delle quantità prodotte per prodotto, con la possibilità di filtrare per data e prodotto.

---

## Struttura del progetto

```
progetto/
│
├── app.py                 # Codice principale dell'app Flask
├── config.py              # Funzioni di configurazione e generazione dei parametri
├── prodotto.py            # Definizione della classe Prodotto
├── produzione.py          # Funzioni per calcolare i tempi di produzione
├── storic_produzione.csv  # File CSV per lo storico della produzione
├── templates/             # Cartella contenente i template HTML
│   └── dashboard.html     # Template HTML per la dashboard
└── static/                # Cartella contenente file statici (JS, CSS)
    ├── dashboard.js       # Script JavaScript per la dashboard
    └── styles.css         # Stile CSS per la dashboard
