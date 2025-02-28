import streamlit as st
import pandas as pd
import plotly.express as px
from youtube_api import YouTubeAnalyzer
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="YouTube Trend Analyzer",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("YouTube Trend Analyzer")
st.markdown("Analyseur de tendances YouTube par niche")
st.markdown("Découvrez les vidéos les plus populaires du dernier mois pour n'importe quelle niche")

# Sidebar
st.sidebar.header("Configuration")

# API Key section with instructions
st.sidebar.subheader("Clé API YouTube")
with st.sidebar.expander("Comment obtenir votre clé API YouTube ?"):
    st.markdown("""
    1. Allez sur [Google Cloud Console](https://console.cloud.google.com)
    2. Créez un nouveau projet ou sélectionnez un projet existant
    3. Activez l'API YouTube Data API v3 :
        - Menu ☰ > APIs & Services > Enable APIs & Services
        - Recherchez "YouTube Data API v3"
        - Cliquez sur "Enable"
    4. Créez une clé API :
        - Menu ☰ > APIs & Services > Credentials
        - Click "+ Create Credentials" > API key
    5. Copiez la clé générée et collez-la ci-dessous
    """)
api_key = st.sidebar.text_input("Entrez votre clé API", type="password")

# Search parameters
st.sidebar.subheader("Paramètres de recherche")
search_mode = st.sidebar.radio(
    "Mode de recherche",
    ["IA Business (mots-clés prédéfinis)", "Recherche personnalisée"]
)

if search_mode == "Recherche personnalisée":
    search_query = st.sidebar.text_input("Niche/Sujet à analyser", placeholder="Ex: cuisine, gaming, tech...")
else:
    search_query = ""
    st.sidebar.info("Utilisation des mots-clés prédéfinis pour l'IA business")

max_results = st.sidebar.slider("Nombre max de résultats par mot-clé", 10, 50, 25)

if api_key:
    try:
        analyzer = YouTubeAnalyzer(api_key)
        
        with st.spinner("Analyse en cours..." + (f" pour '{search_query}'" if search_query else " pour la niche IA business")):
            # Get and analyze data
            df = analyzer.search_videos(
                query=search_query if search_mode == "Recherche personnalisée" else "",
                use_keywords=search_mode == "IA Business (mots-clés prédéfinis)",
                max_results=max_results
            )
            trends = analyzer.analyze_trends(df)

            if df.empty:
                st.warning("Aucune vidéo trouvée pour cette recherche. Essayez un autre sujet ou augmentez le nombre de résultats.")
            
            if not df.empty:
                # Overview metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Vidéos", trends['total_videos'])
                with col2:
                    st.metric("Total Vues", f"{trends['total_views']:,}")
                with col3:
                    st.metric("Moyenne Vues", f"{trends['avg_views']:,.0f}")
                with col4:
                    st.metric("Moyenne Likes", f"{trends['avg_likes']:,.0f}")

                # Top videos
                st.header("Top 10 Vidéos les Plus Vues")
                if not df.empty:
                    top_videos = df.nlargest(10, 'view_count')[['title', 'channel_title', 'view_count', 'url']]
                    for _, video in top_videos.iterrows():
                        st.markdown(f"### [{video['title']}]({video['url']})")
                        st.markdown(f"**Chaîne:** {video['channel_title']}")
                        st.markdown(f"**Vues:** {video['view_count']:,}")
                        st.markdown("---")

                # Views distribution
                st.header("Distribution des Vues")
                fig = px.histogram(df, x="view_count", nbins=30,
                                 title="Distribution des Vues")
                st.plotly_chart(fig)

                # Top channels
                st.header("Top Chaînes")
                top_channels = pd.DataFrame.from_dict(
                    trends['top_channels'], 
                    orient='index', 
                    columns=['Nombre de vidéos']
                )
                fig = px.bar(top_channels, title="Chaînes les Plus Actives")
                st.plotly_chart(fig)

                # Timeline
                st.header("Timeline des Publications")
                fig = px.scatter(df, x="published_at", y="view_count",
                               hover_data=["title", "channel_title"],
                               title="Vues par Date de Publication")
                st.plotly_chart(fig)

                # Raw data
                st.header("Données Brutes")
                st.dataframe(df)

    except Exception as e:
        st.error(f"Une erreur s'est produite: {str(e)}")
else:
    if not api_key:
        st.info("👆 Veuillez entrer votre clé API YouTube dans la barre latérale pour commencer l'analyse.")
    elif not search_query:
        st.info("🔍 Entrez un sujet ou une niche à analyser dans la barre latérale.")
