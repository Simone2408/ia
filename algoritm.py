import numpy as np
from copy import deepcopy
from itertools import product
from rete_bayesiana import ReteBayesiana

def impara_parametri(rete_originale, dati):
    """
    Apprende CPT da dati usando smoothing di Laplace.
    
    Args:
        rete_originale: Rete con struttura nota (solo genitori/stati)
        dati: Lista di campioni (dizionari)
    
    Returns:
        Nuova rete con CPT apprese
    """
    rete_appresa = deepcopy(rete_originale)
    
    for nome_nodo, nodo in rete_appresa.nodi.items():
        # Inizializza conteggi con Laplace smoothing (tutti a 1)
        conteggi = {}
        
        if not nodo.genitori:
            # Nodo radice: una sola distribuzione
            conteggi["root"] = {stato: 1 for stato in nodo.stati}
        else:
            # Nodo con genitori: una distribuzione per ogni combinazione
            stati_genitori = [rete_appresa.nodi[g].stati for g in nodo.genitori]
            
            for comb_genitori in product(*stati_genitori):
                conteggi[comb_genitori] = {stato: 1 for stato in nodo.stati}
        
        # Conta occorrenze nei dati
        for campione in dati:
            valore_nodo = campione[nome_nodo]
            
            if not nodo.genitori:
                chiave = "root"
            else:
                chiave = tuple(campione[g] for g in nodo.genitori)
            
            conteggi[chiave][valore_nodo] += 1
        
        # Converti conteggi in probabilità
        cpt_nuova = {}
        for chiave, conteggi_locali in conteggi.items():
            totale = sum(conteggi_locali.values())
            
            if chiave == "root":
                # Nodo radice: salva direttamente
                cpt_nuova = {stato: count/totale for stato, count in conteggi_locali.items()}
            else:
                # Nodo con genitori: mantieni struttura annidata
                cpt_nuova[chiave] = {stato: count/totale for stato, count in conteggi_locali.items()}
        
        nodo.cpt = cpt_nuova
    
    return rete_appresa

def kl_divergence(p, q):
    """
    Calcola divergenza KL tra due distribuzioni.
    Gestisce zeri con epsilon per stabilità numerica.
    """
    p, q = np.asarray(p), np.asarray(q)
    
    # Evita log(0) e divisioni per 0
    epsilon = 1e-10
    p = np.where(p == 0, epsilon, p)
    q = np.where(q == 0, epsilon, q)
    
    return np.sum(p * np.log(p / q))

def js_divergence(p, q):
    """Calcola divergenza Jensen-Shannon tra due distribuzioni."""
    p, q = np.asarray(p), np.asarray(q)
    m = 0.5 * (p + q)
    return 0.5 * (kl_divergence(p, m) + kl_divergence(q, m))

def calcola_divergenza_media(rete_vera, rete_appresa):
    """
    Calcola errore medio (JS divergence) tra due reti.
    Confronta ogni distribuzione condizionata.
    """
    divergenze = []
    
    for nome_nodo in rete_vera.nodi:
        nodo_vero = rete_vera.nodi[nome_nodo]
        nodo_appreso = rete_appresa.nodi[nome_nodo]
        
        if not nodo_vero.genitori:
            # Nodo radice: una sola distribuzione
            dist_vera = nodo_vero.cpt
            dist_appresa = nodo_appreso.cpt
            
            # Estrai probabilità nell'ordine degli stati
            p_probs = [dist_vera[stato] for stato in nodo_vero.stati]
            q_probs = [dist_appresa[stato] for stato in nodo_vero.stati]
            
            divergenze.append(js_divergence(p_probs, q_probs))
        else:
            # Nodo con genitori: confronta ogni distribuzione condizionata
            for condizione in nodo_vero.cpt:
                dist_vera = nodo_vero.cpt[condizione]
                dist_appresa = nodo_appreso.cpt[condizione]
                
                # Estrai probabilità nell'ordine degli stati
                p_probs = [dist_vera[stato] for stato in nodo_vero.stati]
                q_probs = [dist_appresa[stato] for stato in nodo_vero.stati]
                
                divergenze.append(js_divergence(p_probs, q_probs))
    
    return np.mean(divergenze) if divergenze else 0.0