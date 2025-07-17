# 📊 Apprendimento Bayesiano dei Parametri in Reti Bayesiane

**Studente:** Simone Suma  
**Matricola:** 7125399

---

## 🎯 Obiettivo

Questo progetto implementa un sistema di **apprendimento Bayesiano dei parametri** in una rete a struttura nota. L'obiettivo è verificare sperimentalmente la **convergenza delle probabilità stimate** al modello reale all'aumentare della dimensione del dataset.

---

## 🧪 Esperimento

L'esperimento segue l'approccio Bayesiano descritto in Heckerman (1997) e si articola in cinque fasi:

1. **Caricamento della rete di riferimento** (ground truth) da file .bif
2. **Generazione di dataset** di dimensioni crescenti tramite **campionamento ancestrale**
3. **Apprendimento dei parametri** utilizzando **smoothing di Laplace** (pseudo-conteggi unitari)
4. **Calcolo dell'errore** tra modello reale e appreso usando **divergenza di Jensen-Shannon (JS)**
5. **Visualizzazione** della curva di apprendimento che mostra la convergenza dell'errore

---

## 📁 Struttura del progetto

```
progetto/
├── main.py                 # Script principale - esegue l'esperimento completo
├── rete_bayesiana.py       # Classi Nodo e ReteBayesiana per struttura e campionamento
├── algoritm.py            # Funzioni di apprendimento parametri e calcolo divergenza JS
├── data/
│   └── asia.bif           # Rete Bayesiana (formato standard BIF)
├── requirements.txt        # Dipendenze Python
└── README.md              
```

### Ruolo dei file principali:

- **`main.py`**: Coordina l'intero esperimento. Carica la rete, genera dataset di dimensioni crescenti (50-10000 campioni), apprende i parametri per ogni dimensione e visualizza la curva di apprendimento finale.

- **`rete_bayesiana.py`**: Definisce la struttura dati per la rete Bayesiana. Include il parser per file BIF, l'ordinamento topologico e il campionamento ancestrale per generare dataset sintetici.

- **`algoritm.py`**: Contiene l'algoritmo di apprendimento dei parametri con smoothing di Laplace e il calcolo della divergenza Jensen-Shannon per confrontare distribuzioni.

---

## ▶️ Esecuzione

### Prerequisiti
- **Python 3.8 o superiore**
- Dipendenze: `numpy`, `matplotlib`

### Comandi per riprodurre i risultati:

```bash
# 1. Installa le dipendenze
pip install -r requirements.txt

# 2. Esegui l'esperimento completo
python main.py

# 3. Visualizza il grafico generato
# Il file 'curva_apprendimento.png' sarà salvato nella directory corrente
```

### Output atteso:
- **Console**: Progress dell'esperimento con errori JS per ogni dimensione dataset
- **Grafico**: Curva di apprendimento salvata come `curva_apprendimento.png`
- **Risultato**: Dimostrazione della convergenza dell'errore al crescere dei dati

---

## 📊 Risultati sperimentali

L'esperimento dimostra che:
- L'errore JS diminuisce all'aumentare della dimensione del dataset
- La convergenza segue un andamento logaritmico caratteristico
- Con 10.000 campioni si ottiene una buona approssimazione del modello reale

---

## 🔧 Dettagli tecnici

- **Metrica di errore**: Divergenza Jensen-Shannon (simmetrica, limitata)
- **Smoothing**: Laplace con pseudo-conteggi unitari per gestire eventi non osservati
- **Campionamento**: Ancestrale seguendo l'ordinamento topologico della rete
- **Rete di test**: "Asia" - rete standard con 8 nodi per diagnosi medica

---

## 📚 Riferimenti

- Heckerman, D. (1997). Bayesian networks for data mining. *Data Mining and Knowledge Discovery*, 1(1), 79-119.
- Formato BIF: Standard per rappresentazione reti Bayesiane