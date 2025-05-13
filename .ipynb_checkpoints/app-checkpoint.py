import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Charger le modèle ML
model = joblib.load('model_pkl/Random Forest_model_retard.pkl')  # Remplace par le chemin réel

# Dictionnaire pour encoder les villes
villes = {
    "Agadir": 0,
    "Marrakech": 2,
    "Rabat": 1,
    "Casablanca": 3,
    "Tanger": 4
}

# === Distances en km entre villes ===
distances = {
    ("Agadir", "Marrakech"): 235,
    ("Agadir", "Rabat"): 570,
    ("Agadir", "Casablanca"): 470,
    ("Agadir", "Tanger"): 865,
    ("Marrakech", "Rabat"): 320,
    ("Marrakech", "Casablanca"): 240,
    ("Marrakech", "Tanger"): 555,
    ("Rabat", "Casablanca"): 95,
    ("Rabat", "Tanger"): 250,
    ("Casablanca", "Tanger"): 340,
}

# === Titre de l'application ===
st.title("🚛 Prédiction du Retard de Camion")

# === Sélection des villes ===
ville_depart = st.selectbox("Ville de départ", list(villes.keys()))
ville_arrivee = st.selectbox("Ville d’arrivée", list(villes.keys()))

# === Calcul automatique de la distance ===
def get_distance(v1, v2):
    if v1 == v2:
        return 0
    return distances.get((v1, v2)) or distances.get((v2, v1)) or 0

distance = get_distance(ville_depart, ville_arrivee)
st.info(f"📏 Distance calculée : *{distance} km*")

# === Poids ===
poids = st.number_input("Poids (kg)", min_value=1)

# === Date & heure de départ ===
date_depart = st.date_input("Date de départ")
heure_depart_time = st.time_input("Heure de départ")
datetime_depart = datetime.combine(date_depart, heure_depart_time)

# === Date & heure d’arrivée ===
date_arrivee = st.date_input("Date d’arrivée")
heure_arrivee_time = st.time_input("Heure d’arrivée")
datetime_arrivee = datetime.combine(date_arrivee, heure_arrivee_time)

# === Checkbox pour weekend et jour férié ===
weekend = st.checkbox("Est-ce un weekend ?", value=datetime_depart.weekday() >= 5)
jour_ferie = st.checkbox("Est-ce un jour férié ?", value=False)

# === Calculs automatiques ===
heure_depart = datetime_depart.hour
heure_arrivee = datetime_arrivee.hour
duree_reelle = int((datetime_arrivee - datetime_depart).total_seconds() // 60)

# === Préparation de la donnée ===
input_data = pd.DataFrame([{
    "Ville de depart": villes[ville_depart],
    "Ville d'arrivee": villes[ville_arrivee],
    "Distance (km)": distance,
    "Poids (kg)": poids,
    "Heure_depart": heure_depart,
    "Heure_arrivee": heure_arrivee,
    "Weekend": int(weekend),
    "Jour ferie": int(jour_ferie),
    "Duree reelle (minutes)": duree_reelle
}])

# === Affichage des données ===
st.subheader("📋 Données envoyées au modèle :")
st.write(input_data)

# === Bouton de prédiction ===
if st.button("Prédire le retard"):
    prediction = model.predict(input_data)[0]
    st.success(f"🔮 Le modèle prédit un retard de *{prediction} minutes*.")