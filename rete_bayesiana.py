import random
import re

class Nodo:
    """Nodo di una rete Bayesiana con genitori, stati e CPT."""
    
    def __init__(self, nome, genitori, cpt):
        self.nome = nome
        self.genitori = genitori  # Lista nomi genitori
        self.cpt = cpt           # Tabella probabilità condizionata
        self.stati = []          # Stati possibili del nodo

    def __str__(self):
        return f"Nodo({self.nome})"

class ReteBayesiana:
    """Rete Bayesiana con nodi, caricamento da file BIF e campionamento."""
    
    def __init__(self):
        self.nodi = {}  # nome_nodo -> oggetto Nodo

    def aggiungi_nodo(self, nodo):
        """Aggiunge un nodo alla rete."""
        self.nodi[nodo.nome] = nodo

    def carica_da_file_bif(self, filepath):
        """Carica rete da file BIF standard."""
        try:
            with open(filepath, 'r') as f:
                contenuto = f.read()
        except FileNotFoundError:
            print(f"Errore: File non trovato a {filepath}")
            return

        # Estrai variabili e i loro stati
        pattern_variabili = r'variable\s+(\w+)\s*\{[^}]*\{([^}]+)\}'
        variabili = re.findall(pattern_variabili, contenuto)
        
        for nome, stati_str in variabili:
            stati = [s.strip() for s in stati_str.split(',')]
            nodo = Nodo(nome=nome, genitori=[], cpt={})
            nodo.stati = stati
            self.aggiungi_nodo(nodo)

        # Estrai probabilità
        pattern_prob = r'probability\s*\(\s*([^)]+)\s*\)\s*\{([^}]+)\}'
        prob_blocks = re.findall(pattern_prob, contenuto)
        
        for prob_def, prob_content in prob_blocks:
            # Parsing della definizione P(figlio|genitori)
            if '|' in prob_def:
                figlio, genitori_str = prob_def.split('|')
                nome_figlio = figlio.strip()
                genitori = [g.strip() for g in genitori_str.split(',')]
            else:
                nome_figlio = prob_def.strip()
                genitori = []
            
            self.nodi[nome_figlio].genitori = genitori
            
            # Parsing del contenuto delle probabilità
            if 'table' in prob_content:
                # Nodo radice: P(X) = [p1, p2, ...]
                table_match = re.search(r'table\s+([^;]+)', prob_content)
                if table_match:
                    prob_values = [float(p) for p in table_match.group(1).replace(',', '').split()]
                    self.nodi[nome_figlio].cpt = dict(zip(self.nodi[nome_figlio].stati, prob_values))
            else:
                # Nodo con genitori: P(X|Y=y) = [p1, p2, ...]
                righe = re.findall(r'\(([^)]+)\)\s+([^;]+)', prob_content)
                for condizione, prob_str in righe:
                    condizione_tuple = tuple(condizione.replace(',', '').split())
                    prob_values = [float(p) for p in prob_str.replace(',', '').split()]
                    self.nodi[nome_figlio].cpt[condizione_tuple] = dict(zip(self.nodi[nome_figlio].stati, prob_values))

        print(f"Rete caricata: {len(self.nodi)} nodi da '{filepath}'")

    def _ordine_topologico(self):
        """Algoritmo di Kahn per ordinamento topologico."""
        # Conta genitori per ogni nodo
        gradi_ingresso = {nome: len(nodo.genitori) for nome, nodo in self.nodi.items()}
        
        # Inizia con nodi senza genitori
        coda = [nome for nome, grado in gradi_ingresso.items() if grado == 0]
        ordinamento = []
        
        while coda:
            nodo_corrente = coda.pop(0)
            ordinamento.append(nodo_corrente)
            
            # Rimuovi archi uscenti e aggiorna gradi
            for nome, nodo in self.nodi.items():
                if nodo_corrente in nodo.genitori:
                    gradi_ingresso[nome] -= 1
                    if gradi_ingresso[nome] == 0:
                        coda.append(nome)
        
        if len(ordinamento) != len(self.nodi):
            raise ValueError("Ciclo rilevato nel grafo")
        
        return ordinamento

    def genera_campione(self):
        """Genera un campione con campionamento ancestrale."""
        campione = {}
        
        # Processa nodi in ordine topologico
        for nome_nodo in self._ordine_topologico():
            nodo = self.nodi[nome_nodo]
            
            # Trova distribuzione appropriata
            if not nodo.genitori:
                # Nodo radice
                distribuzione = nodo.cpt
            else:
                # Nodo con genitori: usa valori dei genitori dal campione corrente
                valori_genitori = tuple(campione[genitore] for genitore in nodo.genitori)
                distribuzione = nodo.cpt[valori_genitori]
            
            # Campiona dal nodo
            stati = list(distribuzione.keys())
            probabilita = list(distribuzione.values())
            campione[nome_nodo] = random.choices(stati, weights=probabilita, k=1)[0]
        
        return campione

    def genera_campioni(self, n):
        """Genera n campioni dalla rete."""
        return [self.genera_campione() for _ in range(n)]

    def stampa_rete(self):
        """Stampa struttura della rete per debug."""
        print("=" * 50)
        print("  STRUTTURA RETE BAYESIANA")
        print("=" * 50)
        print(f"Nodi: {len(self.nodi)}\n")

        try:
            nodi_ordinati = self._ordine_topologico()
        except ValueError as e:
            print(f"Errore ordinamento: {e}")
            nodi_ordinati = list(self.nodi.keys())

        for nome_nodo in nodi_ordinati:
            nodo = self.nodi[nome_nodo]
            print(f"--- {nodo.nome} ---")
            
            # Genitori
            if nodo.genitori:
                print(f"  Genitori: {', '.join(nodo.genitori)}")
            else:
                print("  Genitori: Nessuno")
            
            # CPT
            print("  CPT:")
            if not nodo.genitori:
                # Nodo radice
                for stato, prob in nodo.cpt.items():
                    print(f"    P({nodo.nome}={stato}) = {prob:.4f}")
            else:
                # Nodo con genitori
                for condizione, distribuzione in nodo.cpt.items():
                    cond_str = ", ".join(f"{gen}={val}" for gen, val in zip(nodo.genitori, condizione))
                    print(f"    P({nodo.nome}|{cond_str}):")
                    for stato, prob in distribuzione.items():
                        print(f"      {stato}: {prob:.4f}")
            print()