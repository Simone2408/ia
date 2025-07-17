import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from rete_bayesiana import ReteBayesiana
from algoritm import impara_parametri, calcola_divergenza_media

def main():
    """Esperimento completo: curva di apprendimento Bayesiano con divergenza JS."""
    print("=== ESPERIMENTO CURVA DI APPRENDIMENTO ===")

    # Configurazione esperimento
    dimensioni_dataset = [50, 100, 250, 500, 1000, 2500, 5000, 10000]
    errori_js = []

    # Carica rete di riferimento
    rete_vera = ReteBayesiana()
    rete_vera.carica_da_file_bif("data/asia.bif")
    print(f"Rete di riferimento caricata\n")

    # Esperimento per ogni dimensione
    for n in dimensioni_dataset:
        print(f"Test con {n} campioni...")
        
        # Genera dataset sintetico
        dati_train = rete_vera.genera_campioni(n)
        
        # Apprendi parametri
        rete_appresa = impara_parametri(rete_vera, dati_train)
        
        # Calcola errore
        errore = calcola_divergenza_media(rete_vera, rete_appresa)
        errori_js.append(errore)
        
        print(f"  Errore JS: {errore:.6f}")

    # Visualizzazione risultati
    print("\n=== GENERAZIONE GRAFICO ===")

    # ---  Configurazione dello Stile ---
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': 'Arial', 
        'axes.titlesize': 20,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'axes.spines.top': False,   # Rimuove il bordo superiore del grafico
        'axes.spines.right': False, # Rimuove il bordo destro del grafico
        'axes.titleweight': 'bold',
        'axes.labelpad': 15,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
    })

    # ---  Creazione della figura e degli assi ---
    fig, ax = plt.subplots(figsize=(12, 7))

    # ---  Disegno della curva principale ---
    ax.plot(dimensioni_dataset, errori_js,
            'o-',                                # Stile linea e marcatore
            linewidth=2.5,                       # Spessore della linea
            markersize=8,                        # Dimensione dei marcatori
            color='#005A9C',                     # Colore blu per la linea
            markerfacecolor='#6495ED',            # Colore di riempimento dei marcatori
            markeredgecolor='#005A9C',            # Colore del bordo dei marcatori
            label='Errore JS Medio')

    # ---  Annotazioni dei valori ---
    for x, y in zip(dimensioni_dataset, errori_js):
        ax.annotate(f'{y:.4f}',
                    (x, y),
                    textcoords="offset points",
                    xytext=(0, 15),
                    ha='center',
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.75))

    # ---  Configurazione di titoli, etichette e assi ---
    ax.set_title('Curva di Apprendimento della Rete Bayesiana', pad=20)
    ax.set_xlabel('Dimensione del Dataset')
    ax.set_ylabel('Divergenza Jensen-Shannon (JS)')
    ax.set_xscale('log')

    # --- Creazione della griglia ---
    ax.grid(True, which='major', axis='both', linestyle='--', linewidth=0.5, color='lightgray', zorder=0)
    ax.grid(True, which='minor', axis='x', linestyle=':', linewidth=0.4, color='lightgray', zorder=0)

 
    ax.legend(loc='upper right', frameon=True, shadow=True, facecolor='white', framealpha=0.9)

    # Forza la visualizzazione dei numeri interi sull'asse X 
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.tick_params(axis='x', which='minor', bottom=False) 
    fig.tight_layout(pad=1.5)
    plt.savefig("curva_apprendimento.png", dpi=300, bbox_inches='tight')

    print("Grafico salvato con successo: curva_apprendimento.png")

    plt.show()


if __name__ == "__main__":
    main()