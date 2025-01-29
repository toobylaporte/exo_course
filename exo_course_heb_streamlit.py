import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from transformers import pipeline

# Création de données simulées
np.random.seed(42)
dates = pd.date_range(start='2025-01-01', end='2025-01-29', freq='D')
distances = np.random.randint(180, 220, size=len(dates))  # 200m +/- 20m
times = np.random.randint(25, 35, size=len(dates))  # 30s +/- 5s
heart_rates = np.random.randint(150, 190, size=len(dates))
feelings = np.random.randint(1, 11, size=len(dates))
temperatures = np.random.randint(15, 30, size=len(dates))

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

print(df.head())

sentiment_analyzer = pipeline("sentiment-analysis")

# Conversion des ressentis numériques en texte
feeling_text = {
    1: "Très mauvais", 2: "Mauvais", 3: "Plutôt mauvais", 4: "Moyen", 5: "Correct",
    6: "Assez bon", 7: "Bon", 8: "Très bon", 9: "Excellent", 10: "Parfait"
}
df['FeelingText'] = df['Feeling'].map(feeling_text)


plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Speed'], marker='o')
plt.title('Évolution de la vitesse au fil du temps')
plt.xlabel('Date')
plt.ylabel('Vitesse (m/s)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Analyse de sentiment
sentiments = sentiment_analyzer(df['FeelingText'].tolist())
df['Sentiment'] = [s['label'] for s in sentiments]
df['SentimentScore'] = [s['score'] for s in sentiments]

print(df[['Date', 'Speed', 'FeelingText', 'Sentiment', 'SentimentScore']].head())

correlation_matrix = df[['Speed', 'HeartRate', 'Feeling', 'Temperature', 'SentimentScore']].corr()
print(correlation_matrix)

def generate_recommendations(df):
    recommendations = []
    
    # Analyse de la tendance de vitesse
    speed_trend = df['Speed'].diff().mean()
    if speed_trend > 0:
        recommendations.append("Votre vitesse s'améliore globalement. Continuez ainsi !")
    else:
        recommendations.append("Votre vitesse semble stagner ou diminuer. Essayez d'intensifier vos séances.")
    
    # Analyse de la corrélation entre la vitesse et la fréquence cardiaque
    speed_hr_corr = df['Speed'].corr(df['HeartRate'])
    if speed_hr_corr > 0.5:
        recommendations.append("Il y a une forte corrélation entre votre vitesse et votre fréquence cardiaque. Travaillez sur votre endurance cardiovasculaire.")
    
    # Analyse du sentiment
    if df['SentimentScore'].mean() < 0.5:
        recommendations.append("Votre ressenti général est plutôt négatif. Essayez de varier vos séances pour maintenir la motivation.")
    
    return recommendations

recommendations = generate_recommendations(df)
for rec in recommendations:
    print("- " + rec)
