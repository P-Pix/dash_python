"""Script de téléchargement/préparation des données OWID pour l'application Dash.

Usage:
    python download_data.py           # Télécharge si absent + construit le tidy
    python download_data.py --force   # Force le re-téléchargement
"""
import argparse
from app.data import ensure_local_files, get_dataset, LOCAL_TIDY, LOCAL_ENERGY, LOCAL_EMISSIONS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Forcer le re-téléchargement et la reconstruction")
    args = parser.parse_args()

    ensure_local_files(force=args.force)
    df = get_dataset(force=args.force)
    print(f"Fichiers bruts: {LOCAL_ENERGY.name} / {LOCAL_EMISSIONS.name}")
    print(f"Jeu de données tidy: {LOCAL_TIDY} ({len(df):,} lignes, {df['indicator'].nunique()} indicateurs)")
    print("OK")


if __name__ == "__main__":
    main()
