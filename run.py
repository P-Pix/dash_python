"""Point d'exécution simple de l'application Dash.

Usage:
    python run.py               # démarrage par défaut (localhost:8050)
    PORT=9000 HOST=0.0.0.0 python run.py

Peut servir aussi d'entrée pour gunicorn:
    gunicorn run:server --bind 0.0.0.0:8050
"""
import os
from app.app import create_app

app = create_app()
server = app.server  # pour gunicorn / wsgi

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8050"))
    debug = os.getenv("DEBUG", "true").lower() in {"1", "true", "yes"}
    # Dash 2.17+: utiliser app.run
    app.run(host=host, port=port, debug=debug)
