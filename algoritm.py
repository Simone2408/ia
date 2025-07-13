
import numpy as np
# Importiamo le classi dal nostro file per usarle come "tipi"
from rete_bayesiana import ReteBayesiana, Nodo

def impara_parametri(struttura_rete, dati):
    """
    L'algoritmo di apprendimento con Smoothing di Laplace.
    Prende una struttura di rete (senza CPT) e i dati, e restituisce
    una nuova rete con le CPT apprese.
    """
    rete_appresa = struttura_rete # Partiamo dalla stessa struttura
    
    # Per ogni nodo nella rete...
    # 1. Inizializza una struttura per i conteggi (es. un dizionario).
    # 2. Itera su ogni campione nei `dati`.
    # 3. Aggiorna i conteggi in base ai valori nel campione.
    # 4. Applica lo smoothing di Laplace (aggiungi +1 a ogni conteggio).
    # 5. Normalizza i conteggi per ottenere le probabilità.
    # 6. Inserisci le nuove probabilità nella CPT della rete_appresa.
    
    print("Apprendimento dei parametri completato.")
    return rete_appresa

def kl_divergence(p, q):
    """Calcola la divergenza di Kullback-Leibler."""
    # Attenzione a non fare log(0)!
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def js_divergence(p, q):
    """Calcola la divergenza di Jensen-Shannon."""
    p = np.asarray(p)
    q = np.asarray(q)
    m = 0.5 * (p + q)
    return 0.5 * (kl_divergence(p, m) + kl_divergence(q, m))