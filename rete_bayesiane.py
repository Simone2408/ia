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

   # Dentro la classe ReteBayesiana

    def _ordine_topologico(self):
        """
        Implementazione dell'algoritmo di Kahn per l'ordinamento topologico.
        """
        # Copia dei gradi d'ingresso (numero di genitori) per ogni nodo
        gradi_ingresso = {nome: len(nodo.genitori) for nome, nodo in self.nodi.items()}
        
        # Coda dei nodi con zero genitori
        coda = [nome for nome, grado in gradi_ingresso.items() if grado == 0]
        
        lista_ordinata = []
        
        while coda:
            nome_nodo = coda.pop(0)
            lista_ordinata.append(nome_nodo)
            
            # Per ogni "vicino" del nodo corrente...
            for altro_nome, altro_nodo in self.nodi.items():
                if nome_nodo in altro_nodo.genitori:
                    # ...riduci il suo grado d'ingresso di 1
                    gradi_ingresso[altro_nome] -= 1
                    # Se il suo grado diventa 0, aggiungilo alla coda
                    if gradi_ingresso[altro_nome] == 0:
                        coda.append(altro_nome)
                        
        if len(lista_ordinata) == len(self.nodi):
            return lista_ordinata
        else:
            # Questo succede se c'e' un ciclo nel grafo, ma non nel nostro caso
            raise Exception("Errore: il grafo contiene un ciclo.")
        
        

    def genera_campione(self):

    #Genera un singolo campione dalla rete usando il campionamento ancestrale.

        campione = {}
        nodi_ordinati = self._ordine_topologico()

        # Itera sui nomi dei nodi nell'ordine corretto (genitori prima dei figli)
        for nome_nodo in nodi_ordinati:
            nodo = self.nodi[nome_nodo]
            
            # 1. Trova la distribuzione di probabilita' corretta dalla CPT
            if not nodo.genitori:
                # Caso A: Nodo senza genitori
                distribuzione = nodo.cpt
            else:
                # Caso B: Nodo con genitori
                # Prendi i valori dei genitori dal campione che stiamo costruendo
                valori_genitori = tuple(campione[nome_genitore] for nome_genitore in nodo.genitori)
                distribuzione = nodo.cpt[valori_genitori]

            # 2. Estrai gli stati e le probabilità da quella distribuzione
            stati = list(distribuzione.keys())
            probabilita = list(distribuzione.values())
            
            # 3. Fai una scelta pesata casuale e salvala nel campione
            valore_scelto = random.choices(stati, weights=probabilita, k=1)[0]
            campione[nome_nodo] = valore_scelto
                
        return campione

    def genera_campioni(self, n):
        """
        Genera n campioni dalla rete.
        """
        lista = []

        for _ in range (n):
            campione_generato = self.genera_campione()
            lista.append(campione_generato)
    
        return lista

    # Dentro la classe ReteBayesiana

    def stampa_rete(self):
        """
        Stampa informazioni dettagliate e formattate sulla rete per debug.
        """
        print("=" * 40)
        print("  DEFINIZIONE DELLA RETE BAYESIANA")
        print("=" * 40)
        print(f"La rete contiene {len(self.nodi)} nodi.\n")

        # Usiamo l'ordine topologico per una stampa piu' logica
        try:
            nodi_ordinati = self._ordine_topologico()
        except Exception as e:
            print(f"Errore nell'ordinamento topologico: {e}. Stampo in ordine casuale.")
            nodi_ordinati = list(self.nodi.keys())

        for nome_nodo in nodi_ordinati:
            nodo = self.nodi[nome_nodo]
            print(f"--- NODO: {nodo.nome} ---")
            
            # Stampa i genitori in modo pulito
            if nodo.genitori:
                print(f"  Genitori: {', '.join(nodo.genitori)}")
            else:
                print("  Genitori: Nessuno (Nodo Radice)")

            # Stampa la Tabella di Probabilita' Condizionata (CPT)
            print("  CPT:")
            if not nodo.genitori:
                # Caso A: Nodo senza genitori
                for stato, prob in nodo.cpt.items():
                    print(f"    P({nodo.nome}={stato}) = {prob:.4f}")
            else:
                # Caso B: Nodo con genitori
                for condizione, distribuzione in nodo.cpt.items():
                    # Formatta la condizione per renderla leggibile (es. "smoke=yes, tub=no")
                    cond_str = ", ".join([f"{gen}={val}" for gen, val in zip(nodo.genitori, condizione)])
                    print(f"    Se ({cond_str}):")
                    for stato, prob in distribuzione.items():
                        print(f"      -> P({nodo.nome}={stato}) = {prob:.4f}")
            
            print() # Aggiunge una riga vuota per separare i nodi

    
# Codice per testare la classe
if __name__ == "__main__":
    mia_rete = ReteBayesiana()
    mia_rete.carica_da_file_bif("asia.bif")
    
    # Test della funzione di stampa
    mia_rete.stampa_rete()
    
    # Test della generazione di campioni
    print("\n--- Genero 3 Campioni di Esempio ---")
    tre_campioni = mia_rete.genera_campioni(1000)
    for i, campione in enumerate(tre_campioni):
        print(f"Campione {i+1}: {campione}")