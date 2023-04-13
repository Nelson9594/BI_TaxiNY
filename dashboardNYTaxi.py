import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
import pydeck as pdk
from PIL import Image


# Title
st.write(
    '<div style="text-align: center; margin: auto;">'
    '<h1>Business Intelligences Project</h1>'
    '<h3>Uber New York</h3>'
    '</div>',
    unsafe_allow_html=True
)

image = Image.open('images/uber.png')

st.image(image)

##########################################

# Load the data
dataset = 'https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv'
df = pd.read_csv(dataset, delimiter=',')

# Show the data as a table
st.write(df)

st.write("Le fichier de données au format CSV à l'URL donnée contient des informations sur les voyages en taxi à New York City. Les données ont été collectées par la Commission des taxis et des limousines de la ville de New York, et couvrent les voyages effectués de janvier à juin 2015.")



##########################################################################################################

st.write(
    '<br><br><br>',
    unsafe_allow_html=True
)

#Metrique 
st.subheader('Metrique')

st.write(
    '<br>',
    unsafe_allow_html=True
)

columns_dep_retr = ['VendorID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']

# Selectionne uniquement la compagnie 1
df_selected_1 = df.loc[df['VendorID'] == 1, columns_dep_retr]
df_selected_1.head()

df_selected_2 = df.loc[df['VendorID'] == 2, columns_dep_retr]

# Calculer la différence entre la colonne 'tpep_dropoff_datetime' et 'tpep_pickup_datetime' de la compagnie 1
df_selected_1['duration'] = pd.to_datetime(df_selected_1['tpep_dropoff_datetime']) - pd.to_datetime(df_selected_1['tpep_pickup_datetime'])
df_selected_2['duration'] = pd.to_datetime(df_selected_2['tpep_dropoff_datetime']) - pd.to_datetime(df_selected_2['tpep_pickup_datetime'])


# Calculer la moyenne de la durée des courses
mean_duration_vendor1 = df_selected_1['duration'].mean()
mean_duration_vendor2 = df_selected_2['duration'].mean()

mean_duration_seconds = mean_duration_vendor1.total_seconds()
hours = int(mean_duration_seconds // 3600)
minutes = int((mean_duration_seconds % 3600) // 60)
seconds = int(mean_duration_seconds % 60)

mean_duration_seconds_2 = mean_duration_vendor2.total_seconds()
hours_2 = int(mean_duration_seconds_2 // 3600)
minutes_2 = int((mean_duration_seconds_2 % 3600) // 60)
seconds_2 = int(mean_duration_seconds_2 % 60)

st.caption('Durée moyenne de temps de trajet pour la compagnie 1')

col1, col2, col3 = st.columns(3)

col1.metric("Heure", hours)
col2.metric("Minutes", minutes)
col3.metric("Secondes", seconds)


st.caption('Durée moyenne de temps de trajet pour la compagnie 2')

col1v2, col2v2, col3v2 = st.columns(3)


col1v2.metric("Heure", hours_2)
col2v2.metric("Minutes", minutes_2, "1")
col3v2.metric("Secondes", seconds_2, "38")



##########################################################################################################
st.write(
    '<br><br><br>',
    unsafe_allow_html=True
)

#Comparaison des points de depots et point de retrait
st.subheader('Comparaison des points de depots et point de retrait')

st.write(
    '<br>',
    unsafe_allow_html=True
)

st.text('Colonne selectionné')
code = '''col_long_lat = ['VendorID', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']'''
st.code(code, language='python')

st.write(
    '<br>',
    unsafe_allow_html=True
)

# Sélectionner les colonnes de latitude et de longitude
col_long_lat = ['VendorID', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']
df_long_lat = df[col_long_lat]

# Créer la figure et les axes
fig, ax = plt.subplots(figsize=(15, 15))

#Titre
ax.set_title('Comparaison Point de retrait Bleu - Point de depot Jaune')

# Définir les données pour les axes X et Y
pickup_x = df_long_lat['pickup_latitude']
pickup_y = df_long_lat['pickup_longitude']
dropoff_x = df_long_lat['dropoff_latitude']
dropoff_y = df_long_lat['dropoff_longitude']

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


###########################################################################################################

st.write(
    '<br><br><br>',
    unsafe_allow_html=True
)

st.subheader('Course Uber')
# Définir la fonction pour afficher le graphique

st.write(
    '<br>',
    unsafe_allow_html=True
)

st.write('Dans cette partie nous pouvons visualiser les graphique des deux compagnie opérant dans la ville de New York, ci dessous nous pouvons voir le nombre de course par heure.')

st.text('Les colonnes selectionnés et transformer en dateTime sont : ')

code = "df_taxi_1['tpep_pickup_datetime'] = pd.to_datetime(df_taxi_1['tpep_pickup_datetime'])"

st.code(code, language='python')

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

    return fig

# Charger les données dans le DataFrame
df_taxi = df.loc[df['VendorID'] == 1]


st.write(
    '<div style="text-align: center; margin: auto;">'
    '<h1>Compagnie 1</h1>'
    '</div>',
    unsafe_allow_html=True
)

# Afficher le graphique
fig = get_pickup_hours(df_taxi)
st.pyplot(fig)


# Charger les données dans le DataFrame
df_taxi = df.loc[df['VendorID'] == 2]

st.write(
    '<div style="text-align: center; margin: auto;">'
    '<h1>Compagnie 2</h1>'
    '</div>',
    unsafe_allow_html=True
)

# Afficher le graphique
fig = get_pickup_hours(df_taxi)
st.pyplot(fig)


###########################################################################################################

st.write(
    '<br><br><br>',
    unsafe_allow_html=True
)

#Comparaison des points de depots et point de retrait
st.subheader('Heatmap')

st.write(
    '<br>',
    unsafe_allow_html=True
)

st.write("Fréquence de passagers en fonction de l'heure de la prise en charge pour l'ensemble des compagnies")

st.write(
    '<br>',
    unsafe_allow_html=True
)

code = "columns = ['tpep_pickup_datetime', 'passenger_count']"

st.code(code, language='python')

st.write(
    '<br>',
    unsafe_allow_html=True
)

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
    ax.set_xlabel('Heure')
    ax.set_ylabel('Nombre de passagers')

    return fig

# Charger les données dans le DataFrame
df_taxi = df

# Afficher le graphique
fig = get_passenger_heatmap(df_taxi)
st.pyplot(fig)

###########################################################################################################

st.write(
    '<br><br><br>',
    unsafe_allow_html=True
)

#Latitude et Longitude
st.subheader('Histogramme')

st.write(
    '<br>',
    unsafe_allow_html=True
)

st.write('Ci dessous vous trouverez un Heatmap des fréquences de nombre de passager en fonction des horaires')


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


###########################################################################################################



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