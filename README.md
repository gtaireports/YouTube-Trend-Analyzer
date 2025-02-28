# YouTube Trend Analyzer

Une application Streamlit pour analyser les tendances YouTube par niche.

## Fonctionnalités

- Analyse des vidéos les plus populaires du dernier mois
- Deux modes de recherche :
  - Niche IA Business (mots-clés prédéfinis)
  - Recherche personnalisée par sujet
- Visualisations interactives :
  - Top 10 des vidéos les plus vues
  - Distribution des vues
  - Top chaînes dans la niche
  - Timeline des publications

## Démo en ligne

L'application est déployée sur Streamlit Cloud et accessible à l'adresse suivante :
[https://youtube-trend-analyzer-srcyoutube-api-w3z58f.streamlit.app/](https://youtube-trend-analyzer-srcyoutube-api-w3z58f.streamlit.app/)

## Utilisation

1. Obtenez une clé API YouTube depuis la [Google Cloud Console](https://console.cloud.google.com)
2. Entrez votre clé API dans le champ prévu à cet effet
3. Choisissez le mode de recherche (IA Business ou personnalisé)
4. Ajustez le nombre de résultats par mot-clé si nécessaire
5. Explorez les résultats et visualisations

## Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/gtaireports/YouTube-Trend-Analyzer.git
cd YouTube-Trend-Analyzer

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Créer un fichier .env avec votre clé API
echo "YOUTUBE_API_KEY=votre_clé_api" > .env

# Lancer l'application
streamlit run src/app.py
```

## Structure du projet

- `src/app.py` : Interface utilisateur Streamlit
- `src/youtube_api.py` : Logique d'interaction avec l'API YouTube
- `config/keywords.txt` : Liste de mots-clés pour la niche IA Business
- `.env` : Fichier de configuration pour la clé API (non inclus dans le dépôt)

## Licence

MIT
