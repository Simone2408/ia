import matplotlib.pyplot as plt
from rete_bayesiana import ReteBayesiana
from algoritm import impara_parametri, js_divergence

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

def esegui_esperimento_curva_apprendimento():
    """
    Funzione principale che esegue l'intero esperimento per
    generare la curva di apprendimento.
    """
    print("--- Inizio Esperimento Curva di Apprendimento ---")

    # --- 1. SETUP ---
    # Definiamo le dimensioni dei dataset da testare
    dimensioni_campione = [50, 100, 250, 500, 1000, 2500, 5000, 10000]
    risultati_divergenza = [] # Qui salveremo gli errori per ogni dimensione

    # Carichiamo la rete originale che rappresenta la "verita'"
    p_vera = ReteBayesiana()
    p_vera.carica_da_file_bif("andes.bif")
    print("Rete 'vera' (p) caricata con successo.")

    # --- 2. CICLO DI SIMULAZIONE ---
    # Eseguiamo l'esperimento per ogni dimensione del campione
    for n in dimensioni_campione:
        print(f"\nInizio test con n = {n} campioni...")

        # a. Genera i dati di addestramento
        dati_training = p_vera.genera_campioni(n)
        
        # b. Apprendi una nuova rete 'q' dai dati
        q_appresa = impara_parametri(p_vera, dati_training)
        
        # c. Calcola l'errore medio tra la rete vera e quella appresa
        errore = calcola_divergenza_media(p_vera, q_appresa)
        risultati_divergenza.append(errore)
        
        print(f"Test completato per n={n}. Errore (JS Divergence Media): {errore:.6f}")

    # --- 3. VISUALIZZAZIONE DEL RISULTATO (VERSIONE MIGLIORATA) ---
    print("\n--- Generazione del grafico della curva di apprendimento... ---")
    
    # Usiamo uno stile piu' professionale per il grafico
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    # Disegna la linea principale
    ax.plot(dimensioni_campione, risultati_divergenza, marker='o', markersize=8, linestyle='-', color='royalblue', label='Errore Medio (JS Divergence)')
    
    # Aggiunge un'area sfumata sotto la linea per un effetto visivo migliore
    ax.fill_between(dimensioni_campione, risultati_divergenza, alpha=0.1, color='royalblue')

    # Aggiunge etichette con il valore esatto per ogni punto
    for i, txt in enumerate(risultati_divergenza):
        ax.annotate(f'{txt:.4f}', (dimensioni_campione[i], risultati_divergenza[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Impostazioni del grafico
    ax.set_title("Curva di Apprendimento del Modello Bayesiano", fontsize=16, fontweight='bold')
    ax.set_xlabel("Numero di Campioni (n)", fontsize=12)
    ax.set_ylabel("Errore Medio (Divergenza JS)", fontsize=12)
    ax.set_xscale('log') # La scala logaritmica e' fondamentale
    
    # Migliora la griglia
    ax.grid(True, which="both", linestyle='--', linewidth=0.5)
    
    # Aggiunge una legenda
    ax.legend()
    
    # Rimuove le cornici superflue per un look piu' pulito
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Salva il grafico in un file
    plt.tight_layout() # Ottimizza lo spazio
    plt.savefig("curva_apprendimento_migliorata.png", dpi=300) # Salva in alta risoluzione
    print("Grafico 'curva_apprendimento_migliorata.png' salvato con successo.")
    
    # Mostra il grafico a schermo
    plt.show()


# Questo blocco viene eseguito solo quando lanci "python main.py"
if __name__ == "__main__":
    esegui_esperimento_curva_apprendimento()
