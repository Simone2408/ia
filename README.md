# 📊 Apprendimento Bayesiano dei Parametri in Reti Bayesiane

**Studente:** Simone Suma  
**Matricola:** 7125399

---

## 🎯 Obiettivo

Questo progetto implementa un sistema di **apprendimento Bayesiano dei parametri** in una rete a struttura nota. L’obiettivo è verificare sperimentalmente la **convergenza delle probabilità stimate** al modello reale all’aumentare della dimensione del dataset.

---

## 🧪 Esperimento

L’esperimento si articola in cinque fasi principali:

1. **Caricamento della rete di riferimento** (ground truth) dal file `asia.bif`.
2. **Generazione di dataset** di dimensioni crescenti tramite **campionamento ancestrale**.
3. **Apprendimento dei parametri** utilizzando **smoothing di Laplace** (pseudo-conteggi iniziali).
4. **Calcolo dell’errore** tra il modello reale e quello appreso, utilizzando la **divergenza di Jensen-Shannon (JS)** come metrica di confronto.
5. **Visualizzazione grafica** della curva di apprendimento, che mostra l'andamento dell’errore rispetto alla quantità di dati.

---

## 📁 Struttura del progetto

- `main.py`: Esegue l’intero esperimento e produce il grafico finale.
- `rete_bayesiana.py`: Contiene le classi `Nodo` e `ReteBayesiana`.
- `algoritmi.py`: Include le funzioni di apprendimento e di confronto tra modelli.
- `asia.bif`: Rete Bayesiana utilizzata come riferimento.
- `requirements.txt`: File delle dipendenze Python.

---

## ▶️ Esecuzione

Assicurati di avere **Python 3.8 o superiore** installato. Poi, installa le dipendenze richieste ed esegui il progetto:

```bash
pip install -r requirements.txt
python3 main.py
