import socket, sys, platform, os
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

# --- single-instance guard (TCP localhost) ------------------------------------


def acquire_single_instance(port=54321, logger=None):
    """
    Acquire an exclusive localhost TCP port to ensure single instance.
    If another instance is running, show a message and exit the process.
    Returns the bound socket; keep it referenced for the entire app lifetime.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Hardening / restart friendliness
    if platform.system() == "Windows":
        # Must be set before bind; prevents others from binding same addr/port while we're alive.
        SO_EXCLUSIVEADDRUSE = getattr(socket, "SO_EXCLUSIVEADDRUSE", 0xFFFFFF)
        try:
            s.setsockopt(socket.SOL_SOCKET, SO_EXCLUSIVEADDRUSE, 1)
        except OSError:
            pass
    else:
        # Helps quick restarts after crashes (does NOT let another process steal the port)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Localhost only: no external exposure
        s.bind(("127.0.0.1", port))
        s.listen(1)  # keep the port reserved; no need to accept
    except OSError:
        # Optional: nice message via Tk if available; otherwise stderr
        try:
            import tkinter as tk
            from tkinter import messagebox
            r = tk.Tk(); r.withdraw()
            messagebox.showinfo("Already running",
                                "The application is already running.\n"
                                "Close the other window to start a new one.")
            r.destroy()
        except Exception as e:
            logger.error(f"Failed to run Tkinter message box: {e}")
            logger.warning("Another instance is already running.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to acquire port: {e}")

    return s
# ------------------------------------------------------------------------------
