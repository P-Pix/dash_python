# Tableau de bord Dash : Energie & CO2

Ce projet est un exemple complet d'application Dash en Python permettant d'explorer des données publiques sur la consommation d'énergie primaire et les émissions de CO2 (Our World In Data) pour présenter les capacités de Dash.

## Fonctionnalités
- Téléchargement dynamique des jeux de données OWID (énergie & CO2)
- Sélection d'indicateurs (énergie, CO2 total, CO2 par habitant)
- Filtrage multi-pays et plage d'années
- Graphique séries temporelles interactif
- Carte choroplèthe (dernière année sélectionnée)
- Heatmap de comparaison (pays vs années)
- Options : échelle logarithmique, normalisation par habitant

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancement
```bash
python -m app.app
```
Ouvrir ensuite http://localhost:8050

## Structure du projet
```
app/
  app.py          # Point d'entrée Dash
  layout.py       # Construction du layout (UI)
  callbacks.py    # Callbacks et logique interactive
  data.py         # Téléchargement + préparation des données
requirements.txt
README.md
```

## Améliorations possibles
- Cache disque (ex: job de pré-téléchargement ou cache Redis)
- Export CSV / PNG des visualisations
- Ajout de tests (pytest) et CI
- Conteneurisation Docker pour déploiement
- Ajout d'autres indicateurs (intensité carbone, part ENR, etc.)

## Données & Licence
Source : Our World In Data (energy-data, co2-data) – licence CC-BY. Citer la source lors de toute réutilisation.