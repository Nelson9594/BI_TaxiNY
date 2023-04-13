import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
import pydeck as pdk


# Title
st.title('Business Intelligences Project')
st.subheader('NY Taxi')

# Load the data
dataset = 'https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv'
df = pd.read_csv(dataset, delimiter=',')

# Show the data as a table
st.write(df)

#Comparaison des points de depots et point de retrait
st.subheader('Comparaison des points de depots et point de retrait')

# Sélectionner les colonnes de latitude et de longitude
col_long_lat = ['VendorID', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']
df_taxi_long_lat = df[col_long_lat]

# Créer la figure et les axes
fig, ax = plt.subplots(figsize=(15, 15))

#Titre
ax.set_title('Comparaison Point de retrait Bleu - Point de depot Jaune')

# Définir les données pour les axes X et Y
pickup_x = df_taxi_long_lat['pickup_latitude']
pickup_y = df_taxi_long_lat['pickup_longitude']
dropoff_x = df_taxi_long_lat['dropoff_latitude']
dropoff_y = df_taxi_long_lat['dropoff_longitude']

# Afficher les données sous forme de nuage de points
ax.scatter(pickup_x, pickup_y, s=0.7, alpha=0.4, c='blue')
ax.scatter(dropoff_x, dropoff_y, s=0.7, alpha=0.4, c='yellow')

# Définir les limites de l'axe X et Y
ax.set_xlim((40.7, 40.9))
ax.set_ylim((-74.1, -73.8))

# Définir les étiquettes de l'axe X et Y
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')

# Afficher la figure dans Streamlit
st.pyplot(fig)





st.subheader('Vendor 1')
# Définir la fonction pour afficher le graphique
def get_pickup_hours(df_taxi):
    df_taxi_1 = df_taxi
    df_taxi_1['tpep_pickup_datetime'] = pd.to_datetime(df_taxi_1['tpep_pickup_datetime'])

    df_taxi_1['hour'] = df_taxi_1['tpep_pickup_datetime'].dt.hour
    df_taxi_1['minute'] = df_taxi_1['tpep_pickup_datetime'].dt.minute

    df_count = df_taxi_1.groupby(['hour', 'minute']).size().reset_index(name='count')

    fig, ax = plt.subplots()
    ax.bar(df_count['hour'] + df_count['minute'] / 60, df_count['count'], width=0.01)
    ax.set_xlabel('Heure')
    ax.set_ylabel('Nombre de courses')
    ax.set_title('Nombre de courses en fonction de l\'heure et de la minute de la prise en charge')

    return fig

# Charger les données dans le DataFrame
df_taxi = df.loc[df['VendorID'] == 1]

# Afficher le graphique
fig = get_pickup_hours(df_taxi)
st.pyplot(fig)


st.subheader('Vendor 2')
# Charger les données dans le DataFrame
df_taxi = df.loc[df['VendorID'] == 2]

# Afficher le graphique
fig = get_pickup_hours(df_taxi)
st.pyplot(fig)




#Comparaison des points de depots et point de retrait
st.subheader('Heatmap')

# Définir la fonction pour afficher le graphique
def get_passenger_heatmap(df_taxi):
    # Sélectionner les colonnes pertinentes
    columns = ['tpep_pickup_datetime', 'passenger_count']
    df_taxi = df_taxi[columns]

    # Convertir la colonne de dates en datetime
    df_taxi['tpep_pickup_datetime'] = pd.to_datetime(df_taxi['tpep_pickup_datetime'])

    # Extraire l'heure à partir de la colonne de dates
    df_taxi['hour'] = df_taxi['tpep_pickup_datetime'].dt.hour

    # Calculer le nombre de courses pour chaque heure et nombre de passagers
    df_count = df_taxi.groupby(['hour', 'passenger_count']).size().reset_index(name='count')

    # Pivoter les données pour avoir le nombre de courses pour chaque heure et nombre de passagers
    # sous forme d'un tableau
    df_pivot = df_count.pivot(index='passenger_count', columns='hour', values='count')

    # Afficher un heatmap des données
    fig, ax = plt.subplots()
    sns.heatmap(df_pivot, cmap='flare')
    ax.set_title('Fréquences de passagers en fonction de l\'heure de la prise en charge')
    ax.set_xlabel('Heure')
    ax.set_ylabel('Nombre de passagers')

    return fig

# Charger les données dans le DataFrame
df_taxi = df

# Afficher le graphique
fig = get_passenger_heatmap(df_taxi)
st.pyplot(fig)


#latitude
st.subheader('Histo Latittude')


# Définir la fonction pour créer les histogrammes
def get_dropoff_histograms(df_taxi):
    # Extraire les variables d'intérêt pour l'histogramme
    lat = df_taxi['dropoff_latitude']
    long = df_taxi['dropoff_longitude']

    # Créer un graphique en barres de la fréquence de dépôt sur la latitude
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.hist(lat, bins=100, color='purple')
    ax2.set_xlabel('Latitude')
    ax2.set_ylabel('Fréquence')
    ax2.set_title('Fréquence de dépôt sur la latitude')

    # Créer un graphique en barres de la fréquence de dépôt sur la longitude
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.hist(long, bins=100, color='orange')
    ax3.set_xlabel('Longitude')
    ax3.set_ylabel('Fréquence')
    ax3.set_title('Fréquence de dépôt sur la longitude')

    # Afficher les graphiques
    st.pyplot(fig2)
    st.pyplot(fig3)

# Charger les données dans le DataFrame
df_taxi = df

# Créer les histogrammes
get_dropoff_histograms(df_taxi)



#maps
st.subheader('Maps')

# Extraire les variables d'intérêt pour la carte
lat = df['pickup_latitude']
long = df['pickup_longitude']

# Créer une carte 3D avec Pydeck
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=lat.mean(),
        longitude=long.mean(),
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df_taxi,
            get_position='[pickup_longitude, pickup_latitude]',
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))