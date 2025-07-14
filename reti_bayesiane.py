import random
import re

class Nodo:
    """
    Rappresenta un singolo nodo nel grafo della Rete Bayesiana.
    """
    def __init__(self, nome, genitori, cpt):
        self.nome = nome
        self.genitori = genitori  # Lista di stringhe con i nomi dei genitori
        self.cpt = cpt           # Una tabella (es. dizionario) di probabilità
        self.stati = []          # Lista degli stati possibili del nodo

    def __str__(self):
        return f"Nodo({self.nome})"

class ReteBayesiana:
    """
    Rappresenta l'intera Rete Bayesiana, come un insieme di nodi.
    """
    def __init__(self):
        self.nodi = {}  # Un dizionario che mappa i nomi dei nodi ai loro oggetti Nodo

    def aggiungi_nodo(self, nodo):
        """Aggiunge un oggetto Nodo alla rete."""
        self.nodi[nodo.nome] = nodo

    def carica_da_file_bif(self, filepath):
        """
        Legge un file .bif e popola la rete con Nodi, Genitori e CPT.
        """
        try:
            with open(filepath, 'r') as f:
                contenuto = f.read()
        except FileNotFoundError:
            print(f"Errore: File non trovato a {filepath}")
            return

        # Trova tutte le variabili
        variabili = re.findall(r'variable\s+(\w+)\s*\{[^}]*\{([^}]+)\}', contenuto)
        
        for nome, stati_str in variabili:
            stati = [s.strip() for s in stati_str.split(',')]
            nuovo_nodo = Nodo(nome=nome, genitori=[], cpt={})
            nuovo_nodo.stati = stati
            self.aggiungi_nodo(nuovo_nodo)

        # Trova tutte le probabilità
        probabilita_blocks = re.findall(r'probability\s*\(\s*([^)]+)\s*\)\s*\{([^}]+)\}', contenuto)
        
        for prob_def, prob_content in probabilita_blocks:
            # Analizza la definizione della probabilità
            if '|' in prob_def:
                parts = prob_def.split('|')
                nome_figlio = parts[0].strip()
                genitori = [g.strip() for g in parts[1].split(',')]
            else:
                nome_figlio = prob_def.strip()
                genitori = []
            
            # Aggiorna i genitori del nodo
            self.nodi[nome_figlio].genitori = genitori
            
            # Analizza il contenuto delle probabilità
            if 'table' in prob_content:
                # Nodo senza genitori
                table_match = re.search(r'table\s+([^;]+)', prob_content)
                if table_match:
                    probs_str = table_match.group(1).replace(',', '').split()
                    probs = [float(p) for p in probs_str]
                    self.nodi[nome_figlio].cpt = dict(zip(self.nodi[nome_figlio].stati, probs))
            else:
                # Nodo con genitori
                righe = re.findall(r'\(([^)]+)\)\s+([^;]+)', prob_content)
                for condizione, probs_str in righe:
                    key_tuple = tuple(condizione.replace(',', '').split())
                    probs = [float(p) for p in probs_str.replace(',', '').split()]
                    self.nodi[nome_figlio].cpt[key_tuple] = dict(zip(self.nodi[nome_figlio].stati, probs))

        print(f"Rete '{filepath}' caricata con successo. Trovati {len(self.nodi)} nodi.")

    def _ordine_topologico(self):
        """
        Restituisce una lista dei nomi dei nodi in ordine topologico
        (i genitori vengono sempre prima dei figli).
        """
        pass

    def genera_campione(self):
        """
        Genera un singolo campione dalla rete usando il campionamento ancestrale.
        """
        pass

    def genera_campioni(self, n):
        """
        Genera n campioni dalla rete.
        """
        pass

    def stampa_rete(self):
        """
        Stampa informazioni sulla rete per debug.
        """
        pass

    def probabilita_evidenza(self, evidenza, n_campioni=10000):
        """
        Stima la probabilità di un'evidenza usando il campionamento.
        evidenza: dizionario con variabile -> valore
        """
        pass

# Codice per testare la classe
if __name__ == "__main__":
    mia_rete = ReteBayesiana()
    mia_rete.carica_da_file_bif("asia.bif")
    
    # Test della funzione di caricamento
    print("\n=== NODI CARICATI ===")
    for nome, nodo in mia_rete.nodi.items():
        print(f"Nodo: {nome}")
        print(f"  Stati: {nodo.stati}")
        print(f"  Genitori: {nodo.genitori}")
        print(f"  CPT: {nodo.cpt}")
        print()