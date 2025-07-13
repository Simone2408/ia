# main.py

# Importiamo tutto quello che ci serve dagli altri nostri file
from rete_bayesiana import ReteBayesiana
from algoritmi import impara_parametri, js_divergence

# E le librerie esterne
import matplotlib.pyplot as plt

def esegui_esperimento():
    """
    Funzione principale che esegue l'intero esperimento.
    """
    # --- 1. SETUP ---
    valori_n = [10, 50, 100, 500, 1000, 5000] # Le dimensioni dei dataset
    risultati_js = []
    path_file_bif = "asia.bif"

    # --- 2. CARICAMENTO DELLA RETE "VERA" ---
    p_vera = ReteBayesiana()
    p_vera.carica_da_file_bif(path_file_bif)
    print("Rete 'vera' caricata con successo.")

    # --- 3. SIMULAZIONE (IL CICLO PRINCIPALE) ---
    for n in valori_n:
        print(f"\nInizio esperimento per n = {n}...")
        # a. Genera n campioni dalla rete vera
        dati_generati = [p_vera.genera_campione() for _ in range(n)]
        
        # b. Impara la nuova rete q_n dai dati
        q_n_appresa = impara_parametri(p_vera, dati_generati) # Passiamo la struttura di p_vera
        
        # c. Calcola la divergenza media tra le CPT di p e q
        divergenza_totale = 0
        # ... qui va la logica per confrontare ogni CPT di p_vera e q_n_appresa ...
        # ... e calcolare la media delle loro divergenze JS ...
        
        risultati_js.append(divergenza_totale)
        print(f"Completato per n={n}, Divergenza JS Media = {divergenza_totale:.4f}")

    # --- 4. VISUALIZZAZIONE ---
    plt.figure(figsize=(10, 6))
    plt.plot(valori_n, risultati_js, marker='o', linestyle='-')
    plt.xscale('log')
    plt.xlabel("Numero di Campioni (n) - Scala Logaritmica")
    plt.ylabel("Divergenza Jensen-Shannon Media")
    plt.title("Curva di Apprendimento")
    plt.grid(True)
    plt.savefig("curva_apprendimento.png")
    print("\nGrafico 'curva_apprendimento.png' salvato con successo.")

# Questo permette di eseguire lo script lanciando "python main.py"
if __name__ == "__main__":
    esegui_esperimento()