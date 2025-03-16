import subprocess
import os
import time
import argparse
import webbrowser
import signal
import sys

api_process = None
ui_process = None


def signal_handler(sig, frame):
    """Gère l'arrêt propre des processus lors de l'interruption (Ctrl+C)"""
    print("\nArrêt des services...")
    if api_process:
        api_process.terminate()
    if ui_process:
        ui_process.terminate()
    print("Services arrêtés.")
    sys.exit(0)


def check_service_ready(port, max_attempts=20, wait_time=0.5):
    """Vérifie si un service est prêt sur le port spécifié"""
    import socket

    attempts = 0
    while attempts < max_attempts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        time.sleep(wait_time)
        attempts += 1
    return False


if __name__ == "__main__":
    # Configurer l'analyseur d'arguments
    parser = argparse.ArgumentParser(description="Lanceur de l'application chatbot-RAG")
    parser.add_argument(
        "--api-only", action="store_true", help="Lancer uniquement l'API"
    )
    parser.add_argument(
        "--ui-only",
        action="store_true",
        help="Lancer uniquement l'interface utilisateur",
    )
    parser.add_argument(
        "--api-port", type=int, default=8000, help="Port pour l'API (défaut: 8000)"
    )
    parser.add_argument(
        "--ui-port", type=int, default=7860, help="Port pour l'interface (défaut: 7860)"
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Ne pas ouvrir automatiquement le navigateur",
    )

    args = parser.parse_args()

    # Configuration des variables d'environnement
    os.environ["API_URL"] = f"http://localhost:{args.api_port}"

    # Configuration du gestionnaire de signal pour l'arrêt propre
    signal.signal(signal.SIGINT, signal_handler)

    # api_process = None
    # ui_process = None

    # Démarrer l'API si demandé
    if not args.ui_only:
        print(f"Démarrage de l'API sur le port {args.api_port}...")
        api_cmd = [sys.executable, "app.py"]
        api_process = subprocess.Popen(
            api_cmd, env={**os.environ, "PORT": str(args.api_port)}
        )

        # Attendre que l'API soit prête
        if not check_service_ready(args.api_port):
            print("L'API ne semble pas démarrer correctement.")
            if api_process:
                api_process.terminate()
            sys.exit(1)
        print(f"API démarrée sur http://localhost:{args.api_port}")

    # Démarrer l'interface si demandée
    if not args.api_only:
        print(f"Démarrage de l'interface sur le port {args.ui_port}...")
        ui_cmd = [sys.executable, "interface.py"]
        ui_env = {**os.environ, "GRADIO_SERVER_PORT": str(args.ui_port)}
        ui_process = subprocess.Popen(ui_cmd, env=ui_env)

        # Attendre que l'interface soit prête
        if not check_service_ready(args.ui_port):
            print("L'interface ne semble pas démarrer correctement.")
            if ui_process:
                ui_process.terminate()
            if api_process:
                api_process.terminate()
            sys.exit(1)

        ui_url = f"http://localhost:{args.ui_port}"
        print(f"Interface démarrée sur {ui_url}")

        # Ouvrir le navigateur si demandé
        if not args.no_open:
            webbrowser.open(ui_url)

    print("\nAppuyez sur Ctrl+C pour arrêter les services.")

    # Maintenir le script en exécution
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
