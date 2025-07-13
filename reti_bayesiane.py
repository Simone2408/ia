# rete_bayesiana.py

# In questo file non ti servono molti import, forse solo 'json' o 're' 
# per leggere il file .bif, ma per ora lasciamolo così.
import random 

class Nodo:
    """
    Rappresenta un singolo nodo nel grafo della Rete Bayesiana.
    """
    def __init__(self, nome, genitori, cpt):
        self.nome = nome
        self.genitori = genitori # Lista di stringhe con i nomi dei genitori
        self.cpt = cpt         # Una tabella (es. dizionario) di probabilità

    def __str__(self):
        return f"Nodo({self.nome})"

class ReteBayesiana:
    """
    Rappresenta l'intera Rete Bayesiana, come un insieme di nodi.
    """
    def __init__(self):
        self.nodi = {} # Un dizionario che mappa i nomi dei nodi ai loro oggetti Nodo

    def aggiungi_nodo(self, nodo):
        """Aggiunge un oggetto Nodo alla rete."""
        self.nodi[nodo.nome] = nodo

    def carica_da_file_bif(self, filepath):
        """
        LEGGE un file .bif e popola la rete.
        Questa è la funzione più complessa da scrivere. Dovrai:
        1. Aprire il file.
        2. Leggerlo riga per riga.
        3. Estrarre i nomi delle variabili (nodi).
        4. Per ogni variabile, estrarre i nomi dei genitori.
        5. Estrarre le tabelle di probabilità (CPT).
        6. Creare oggetti Nodo e aggiungerli alla rete con self.aggiungi_nodo().
        """
        with open(filepath, 'r') as file:
            for line in file:
                # Ignora le righe vuote o commentate
                if not line.strip() or line.startswith('#'):
                    continue
                
            print(line)  # Debug: stampa la riga corrente
                # Logica per estrarre nome, genitori e CPT
                # ... (da implementare) ...
                
    def genera_campione(self):
        """
        GENERA un singolo campione dalla rete usando il campionamento ancestrale.
        """
        campione = {}
        nodi_ordinati = self._ordine_topologico() # Funzione ausiliaria da creare

        for nome_nodo in nodi_ordinati:
            nodo = self.nodi[nome_nodo]
            # Calcola la probabilità e genera un valore per questo nodo
            # basandoti sui valori già presenti in `campione` per i suoi genitori.
            # ... logica di campionamento ...
            # campione[nome_nodo] = valore_generato
        
        return campione

    def _ordine_topologico(self):
        """
        (Funzione ausiliaria) Restituisce una lista dei nomi dei nodi 
        in modo che i genitori vengano sempre prima dei figli.
        Questo è fondamentale per il campionamento.
        """
        # ... logica per l'ordinamento topologico ...
        # Per ora, per 'asia.bif', puoi anche scriverlo a mano se ti blocchi.
        return ['Asia', 'Tubercolosis', 'Smoking', 'LungCancer', 'Bronchitis', 'Either', 'XRay', 'Dyspnoea']
    
ReteBayesiana = new ReteBayesiana()
ReteBayesiana.carica_da_file_bif("asia.bif")