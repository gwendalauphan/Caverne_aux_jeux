import sys
from pathlib import Path

def resource_path(relative_path):
    try:
        # Support pour les applications empaquetées avec PyInstaller
        base_path = Path(sys._MEIPASS)
    except Exception:
        # Utilisation du chemin du répertoire du script main.py pour les exécutions non empaquetées
        base_path = Path(__file__).resolve().parent.parent

    # Construction du chemin complet
    full_path = base_path / relative_path

    return str(full_path)
