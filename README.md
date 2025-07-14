# Progetto di Apprendimento dei Parametri per Reti Bayesiane

**Studente:** Simone Suma
**Matricola:** 7125399

---

## 1. Descrizione del Progetto

Questo progetto implementa un algoritmo di **apprendimento Bayesiano dei parametri** per una Rete Bayesiana a struttura nota. L'obiettivo è dimostrare sperimentalmente la convergenza del modello appreso al modello reale all'aumentare della dimensione del dataset di training.

L'esperimento segue i seguenti passi:
1.  Caricamento di una rete di riferimento ("ground truth") dal file `asia.bif`.
2.  Generazione di dataset di training di dimensioni crescenti tramite campionamento ancestrale.
3.  Apprendimento di una nuova rete per ogni dataset, stimando le CPT tramite un approccio Bayesiano con **smoothing di Laplace** (pseudo-conteggi unitari).
4.  Calcolo dell'errore tra la rete vera e quella appresa utilizzando la **Divergenza di Jensen-Shannon (JS)** come metrica di distanza.
5.  Visualizzazione dei risultati tramite una **curva di apprendimento** che mostra la relazione tra la dimensione del campione e l'errore di stima.

## 2. Struttura del Progetto

Il progetto è organizzato nei seguenti file:

* `main.py`: Lo script principale che orchestra l'intero esperimento, esegue la simulazione per le diverse dimensioni del campione e genera il grafico finale della curva di apprendimento.
* `rete_bayesiana.py`: Contiene le classi `Nodo` e `ReteBayesiana`, che definiscono la struttura dati della rete. Include i metodi per caricare una rete da un file `.bif` e per generare campioni.
* `algoritmi.py`: Contiene le funzioni logiche del progetto:
    * `impara_parametri()`: Implementa l'algoritmo di apprendimento Bayesiano con smoothing di Laplace.
    * `js_divergence()`: Implementa la metrica di distanza per confrontare le distribuzioni di probabilità.
* `asia.bif`: Il file di definizione della rete Bayesiana "Asia", utilizzato come ground truth per l'esperimento.

## 3. Prerequisiti

Per eseguire il codice, sono necessarie le seguenti librerie Python. È consigliabile installarle tramite `pip`.

* Python 3.x
* Matplotlib
* NumPy

Puoi installare le dipendenze con il seguente comando:
```bash
pip install matplotlib numpy