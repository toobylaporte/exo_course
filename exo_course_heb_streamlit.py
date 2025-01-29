import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from transformers import pipeline

# Titre de l'application
st.title("Analyse d'entraînement de course")
st.write("Cette application analyse vos données d'entraînement pour vous fournir des insights et des recommandations.")

# Création de données simulées
np.random.seed(42)
dates = pd.date_range(start='2025-01-01', end='2025-01-29', freq='D')
distances = np.random.randint(180, 220, size=len(dates))  # 200m +/- 20m
times = np.random.randint(25, 35, size=len(dates))  # 30s +/- 5s
heart_rates = np.random.randint(150, 190, size=len(dates))
feelings = np.random.randint(1, 11, size=len(dates))
temperatures = np.random.randint(15, 30, size=len(dates))

# Création du DataFrame
df = pd.DataFrame({
    'Date': dates,
    'Distance': distances,
    'Time': times,
    'HeartRate': heart_rates,
    'Feeling': feelings,
    'Temperature': temperatures
})

# Calcul de la vitesse en m/s
df['Speed'] = df['Distance'] / df['Time']

# Affichage des données brutes
st.subheader("Données d'entraînement")
st.write(df)

# Conversion des ressentis numériques en texte
feeling_text = {
    1: "Très mauvais", 2: "Mauvais", 3: "Plutôt mauvais", 4: "Moyen", 5: "Correct",
    6: "Assez bon", 7: "Bon", 8: "Très bon", 9: "Excellent", 10: "Parfait"
}
df['FeelingText'] = df['Feeling'].map(feeling_text)

# Visualisation de l'évolution de la vitesse au fil du temps
st.subheader("Évolution de la vitesse")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['Date'], df['Speed'], marker='o')
ax.set_title('Évolution de la vitesse au fil du temps')
ax.set_xlabel('Date')
ax.set_ylabel('Vitesse (m/s)')
plt.xticks(rotation=45)
st.pyplot(fig)

# Analyse de sentiment avec Hugging Face
st.subheader("Analyse de sentiment basée sur le ressenti")
sentiment_analyzer = pipeline("sentiment-analysis")
sentiments = sentiment_analyzer(df['FeelingText'].tolist())
df['Sentiment'] = [s['label'] for s in sentiments]
df['SentimentScore'] = [s['score'] for s in sentiments]

st.write("Résultats de l'analyse de sentiment :")
st.write(df[['Date', 'FeelingText', 'Sentiment', 'SentimentScore']])

# Matrice de corrélation
st.subheader("Matrice de corrélation")
correlation_matrix = df[['Speed', 'HeartRate', 'Feeling', 'Temperature', 'SentimentScore']].corr()
st.write(correlation_matrix)

# Génération des recommandations
def generate_recommendations(df):
    recommendations = []
    
    # Analyse de la tendance de vitesse
    speed_trend = df['Speed'].diff().mean()
    if speed_trend > 0:
        recommendations.append("✅ Votre vitesse s'améliore globalement. Continuez ainsi !")
    else:
        recommendations.append("⚠️ Votre vitesse semble stagner ou diminuer. Essayez d'intensifier vos séances.")
    
    # Analyse de la corrélation entre la vitesse et la fréquence cardiaque
    speed_hr_corr = df['Speed'].corr(df['HeartRate'])
    if speed_hr_corr > 0.5:
        recommendations.append("✅ Il y a une forte corrélation entre votre vitesse et votre fréquence cardiaque. Travaillez sur votre endurance cardiovasculaire.")
    
    # Analyse du sentiment
    if df['SentimentScore'].mean() < 0.5:
        recommendations.append("⚠️ Votre ressenti général est plutôt négatif. Essayez de varier vos séances pour maintenir la motivation.")
    
    return recommendations

recommendations = generate_recommendations(df)

# Affichage des recommandations
st.subheader("Recommandations personnalisées")
for rec in recommendations:
    st.write("- " + rec)
