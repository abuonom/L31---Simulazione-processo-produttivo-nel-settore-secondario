let dati = {};
let chartInstance;
let storicoData = [];
let storicoFiltrato = [];
let paginaCorrente = 1;
const righePerPagina = 10;
let sortKey = null;
let sortAsc = true;


/*Funzione asincrona che recupera dati da un endpoint specifico. 
In base al tipo di informazioni richieste (quantità, parametri o tempi di produzione). 
Aggiorna dinamicamente l'interfaccia utente mostrando i dati nella tabella.*/
async function fetchData(endpoint, type) {
  document.getElementById("tabellaDati").style.display = "block";
  document.getElementById("graficoView").style.display = "none";
  document.getElementById("storicoView").style.display = "none";

  const response = await fetch(endpoint);
  const data = await response.json();

  if (type === 'quantita') {
    for (let prodotto in data) {
      dati[prodotto] = dati[prodotto] || {};
      dati[prodotto].quantita = data[prodotto];
    }
  } else if (type === 'parametri') {
    for (let prodotto in data.parametri) {
      dati[prodotto] = dati[prodotto] || {};
      dati[prodotto].tempo_unitario = data.parametri[prodotto].tempo_unitario;
      dati[prodotto].capacita_giornaliera = data.parametri[prodotto].capacita_giornaliera;
      dati[prodotto].fasi = data.parametri[prodotto].fasi;
    }
    document.getElementById("capacitaComplessiva").textContent =
      "Capacità Giornaliera Complessiva: " + data.capacita_complessiva + " unità";
  } else if (type === 'tempo') {
    for (let prodotto in data.dettagli) {
      dati[prodotto] = dati[prodotto] || {};
      dati[prodotto].tempo_totale_prodotto = data.dettagli[prodotto].tempo_totale_prodotto;
      dati[prodotto].fasi_singole = data.dettagli[prodotto].fasi_singole;
      dati[prodotto].fasi_totali = data.dettagli[prodotto].fasi_totali;
      dati[prodotto].quantita = data.quantita[prodotto];
    }
    document.getElementById("tempoProduzioneTotale").textContent =
      "Tempo Totale Produzione Lotto: " + data.tempo_totale_ore + " ore (" + data.tempo_totale_giorni + " giorni)";
  }
  renderTable();
}

/*Funzione che si occupa di renderizzare la tabella*/
function renderTable() {
  let output = `
    <table>
      <tr>
        <th>Prodotto</th>
        <th>Quantità</th>
        <th>Tempo Unitario (ore)</th>
        <th>Capacità Giornaliera</th>
        <th>Durata Singola Fase (ore)</th>
        <th>Durata Totale Fasi (ore)</th>
        <th>Tempo Totale Prodotto (ore)</th>
      </tr>`;

  for (let prodotto in dati) {
    let qta = dati[prodotto].quantita || 0;
    let fasiSingole = dati[prodotto].fasi_singole ?
      Object.entries(dati[prodotto].fasi_singole).map(([fase, durata]) => `${fase}: ${durata} h`).join('<br>') : '-';
    let fasiTotali = dati[prodotto].fasi_totali ?
      Object.entries(dati[prodotto].fasi_totali).map(([fase, durata]) => `${fase}: ${durata} h`).join('<br>') : '-';

    output += `
      <tr>
        <td>${prodotto}</td>
        <td>${qta}</td>
        <td>${dati[prodotto].tempo_unitario || '-'}</td>
        <td>${dati[prodotto].capacita_giornaliera || '-'}</td>
        <td>${fasiSingole}</td>
        <td>${fasiTotali}</td>
        <td>${dati[prodotto].tempo_totale_prodotto || '-'}</td>
      </tr>`;
  }
  output += "</table>";
  document.getElementById("tabellaDati").innerHTML = output;
}

function mostraVistaGrafico() {
  document.getElementById("tabellaDati").style.display = "none";
  document.getElementById("graficoView").style.display = "block";
  document.getElementById("storicoView").style.display = "none";
}

/* Funzione per generare il grafico */
async function generaGrafico() {
  const start = document.getElementById('startDate').value;
  const end = document.getElementById('endDate').value;
  const prodottoFiltro = document.getElementById('prodottoSelect').value;
  const response = await fetch('/grafico');
  const storico = await response.json();

  const aggregati = {};
  const giorniSet = new Set();

  storico.forEach(riga => {
    const dataRiga = riga.Data?.slice(0, 10);
    const prodotto = riga.Prodotto;
    const quantita = parseFloat(riga["Quantita"]);
    if (
      dataRiga && prodotto &&
      (!start || dataRiga >= start) &&
      (!end || dataRiga <= end) &&
      !isNaN(quantita)
    ) {
      giorniSet.add(dataRiga);
      if (!aggregati[prodotto]) aggregati[prodotto] = {};
      aggregati[prodotto][dataRiga] = (aggregati[prodotto][dataRiga] || 0) + quantita;
    }
  });

  const giorni = Array.from(giorniSet).sort();
  const datasets = [];

  const colori = {
    "Spaghetti Barilla": "#28a745",
    "Frollini Mulino Bianco": "#007bff",
    "Pesto Barilla": "#ffc107"
  };

  const prodottiDaMostrare = prodottoFiltro === "tutti" ? Object.keys(aggregati) : [prodottoFiltro];

  prodottiDaMostrare.forEach(prodotto => {
    const datiGiornalieri = giorni.map(giorno => aggregati[prodotto]?.[giorno] || 0);
    datasets.push({
      label: prodotto,
      data: datiGiornalieri,
      borderColor: colori[prodotto] || "#000",
      backgroundColor: (colori[prodotto] || "#000") + "44",
      borderWidth: 2,
      tension: 0.3
    });
  });

  const ctx = document.getElementById('graficoProduzione').getContext('2d');
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: giorni,
      datasets: datasets
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Quantità prodotta"
          }
        },
        x: {
          title: {
            display: true,
            text: "Giorno"
          }
        }
      }
    }
  });
}

async function mostraStorico() {
  document.getElementById("tabellaDati").style.display = "none";
  document.getElementById("graficoView").style.display = "none";
  document.getElementById("storicoView").style.display = "block";

  const response = await fetch('/grafico');
  storicoData = await response.json();
  applicaFiltriStorico();
}

function applicaFiltriStorico() {
  const filtro = document.getElementById("filtroProdotto").value.toLowerCase();
  const da = document.getElementById("filtroDataDa").value;
  const a = document.getElementById("filtroDataA").value;

  storicoFiltrato = storicoData.filter(row => {
    const prodotto = row.Prodotto?.toLowerCase() || '';
    const data = row.Data || '';
    return prodotto.includes(filtro) &&
      (!da || data >= da) &&
      (!a || data <= a);
  });

  if (sortKey) {
    storicoFiltrato.sort((a, b) => {
      const valA = a[sortKey];
      const valB = b[sortKey];

      if (!isNaN(valA) && !isNaN(valB)) {
        return sortAsc ? valA - valB : valB - valA;
      } else {
        return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
      }
    });
  }

  paginaCorrente = 1;
  renderStoricoPaginato();
}

function renderStoricoPaginato() {
  const inizio = (paginaCorrente - 1) * righePerPagina;
  const fine = inizio + righePerPagina;
  const pagina = storicoFiltrato.slice(inizio, fine);

  let html = `<table><tr>
    ${["Data", "Prodotto", "Quantita", "Tempo Totale (ore)", "Tempo Totale (giorni)"].map(key =>
    `<th onclick="ordinaPerColonna('${key}')">${key} ⬍</th>`).join("")}
    </tr>`;

  pagina.forEach(row => {
    html += `<tr>
      <td>${row.Data}</td>
      <td>${row.Prodotto}</td>
      <td>${row.Quantita}</td>
      <td>${row["Tempo Totale (ore)"]}</td>
      <td>${row["Tempo Totale (giorni)"]}</td>
    </tr>`;
  });

  html += `</table>`;

  const totalePagine = Math.ceil(storicoFiltrato.length / righePerPagina);
  html += `
    <div style="margin-top:10px;">
      <button ${paginaCorrente === 1 ? 'disabled' : ''} onclick="paginaCorrente--; renderStoricoPaginato()">◀️ Precedente</button>
      <span style="margin: 0 10px;">Pagina ${paginaCorrente} di ${totalePagine}</span>
      <button ${paginaCorrente === totalePagine ? 'disabled' : ''} onclick="paginaCorrente++; renderStoricoPaginato()">Successivo ▶️</button>
    </div>`;

  document.getElementById("storicoTable").innerHTML = html;
}

function ordinaPerColonna(colonna) {
  if (sortKey === colonna) {
    sortAsc = !sortAsc;
  } else {
    sortKey = colonna;
    sortAsc = true;
  }
  applicaFiltriStorico();
}

function tornaAllaTabella() {
  document.getElementById("graficoView").style.display = "none";
  document.getElementById("storicoView").style.display = "none";
  document.getElementById("tabellaDati").style.display = "block";
}