# algoritmi.py
import numpy as np
from copy import deepcopy
from itertools import product

from rete_bayesiana import ReteBayesiana # Assicurati che rete_bayesiana.py sia nella stessa cartella

def impara_parametri(struttura_rete, dati):
    """
    Versione robusta che inizializza tutti i possibili conteggi a 1
    per gestire anche le condizioni non osservate nei dati.
    """
    rete_appresa = deepcopy(struttura_rete)
    
    for nome_nodo, nodo in rete_appresa.nodi.items():
        conteggi = {}
        
        # Inizializza i conteggi per tutte le possibili combinazioni dei genitori
        if not nodo.genitori:
            # Nodo senza genitori - usa "no_parents" come chiave
            conteggi["no_parents"] = {}
            for stato in nodo.stati:
                conteggi["no_parents"][stato] = 1
        else:
            # Nodo con genitori - genera tutte le combinazioni possibili
            stati_genitori = []
            for g in nodo.genitori:
                stati_genitori.append(rete_appresa.nodi[g].stati)
            
            # Genera tutte le combinazioni possibili dei valori dei genitori
            for combinazione_genitori in product(*stati_genitori):
                # Usa sempre la tupla come chiave (come nel file BIF originale)
                conteggi[combinazione_genitori] = {}
                for stato in nodo.stati:
                    conteggi[combinazione_genitori][stato] = 1
        
        # Ciclo sui dati per aggiornare i conteggi
        for campione in dati:
            risultato = campione[nome_nodo]
            
            if not nodo.genitori:
                condizione = "no_parents"
            else:
                # Costruisci la tupla dei valori dei genitori per questo campione
                valori_genitori = []
                for g_nome in nodo.genitori:
                    valori_genitori.append(campione[g_nome])
                condizione = tuple(valori_genitori)
            
            conteggi[condizione][risultato] += 1
        
        # Trasforma i conteggi in probabilità
        cpt_appresa = {}
        for condizione, conteggi_locali in conteggi.items():
            totale_conteggi = sum(conteggi_locali.values())
            if condizione == "no_parents":
                # Per nodi senza genitori, salva direttamente nel formato originale
                for stato, conteggio in conteggi_locali.items():
                    cpt_appresa[stato] = conteggio / totale_conteggi
            else:
                # Per nodi con genitori, mantieni la struttura a dizionario annidato
                distribuzione_prob = {}
                for stato, conteggio in conteggi_locali.items():
                    distribuzione_prob[stato] = conteggio / totale_conteggi
                cpt_appresa[condizione] = distribuzione_prob
        
        nodo.cpt = cpt_appresa
    
    print("Apprendimento dei parametri completato.")
    return rete_appresa

def kl_divergence(p: list, q: list) -> float:
    """
    Calcola la Divergenza di Kullback-Leibler con gestione robusta degli zeri.
    """
    p = np.asarray(p)
    q = np.asarray(q)
    
    # Aggiungi un piccolo valore epsilon per evitare log(0) e divisioni per zero
    epsilon = 1e-10
    p = np.where(p == 0, epsilon, p)
    q = np.where(q == 0, epsilon, q)
    
    # Calcola KL divergence
    return np.sum(p * np.log(p / q))

def js_divergence(p: list, q: list) -> float:
    """
    Calcola la Divergenza di Jensen-Shannon.
    """
    p = np.asarray(p)
    q = np.asarray(q)
    m = 0.5 * (p + q)
    return 0.5 * (kl_divergence(p, m) + kl_divergence(q, m))

def calcola_divergenza_media(rete_vera, rete_appresa):
    """
    Calcola l'errore medio (Divergenza JS) tra due reti.
    Confronta ogni CPT della rete vera con quella appresa.
    """
    divergenze_locali = []
    for nome_nodo in rete_vera.nodi:
        nodo_vero = rete_vera.nodi[nome_nodo]
        nodo_appreso = rete_appresa.nodi[nome_nodo]
        
        # --- CORREZIONE: Gestiamo i due tipi di CPT separatamente ---
        if not nodo_vero.genitori:
            # CASO A: Nodo senza genitori
            dist_vera = nodo_vero.cpt
            dist_appresa = nodo_appreso.cpt.get("no_parents", {}) # La nostra chiave fissa
            
            if not dist_appresa: continue # Salta se per qualche motivo la CPT appresa è vuota

            stati = nodo_vero.stati
            p_probs = [dist_vera.get(stato, 0) for stato in stati]
            q_probs = [dist_appresa.get(stato, 0) for stato in stati]
            
            divergenza = js_divergence(p_probs, q_probs)
            divergenze_locali.append(divergenza)
        else:
            # CASO B: Nodo con genitori
            # Itera su ogni condizione (riga) della CPT
            for condizione, dist_vera in nodo_vero.cpt.items():
                dist_appresa = nodo_appreso.cpt[condizione]
                
                # Estrai le liste di probabilità da confrontare
                stati = nodo_vero.stati
                p_probs = [dist_vera[stato] for stato in stati]
                q_probs = [dist_appresa[stato] for stato in stati]
                
                # Calcola la divergenza per questa singola distribuzione
                divergenza = js_divergence(p_probs, q_probs)
                divergenze_locali.append(divergenza)
    
    # Restituisce la media di tutte le divergenze calcolate
    if not divergenze_locali:
        return 0
    return sum(divergenze_locali) / len(divergenze_locali)
