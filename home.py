import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Title
st.title('Business Intelligences Project')
st.subheader('Emplois')

# Load the data
dataset = '/Users/nelson/Desktop/BI_streamlit/data/normDataset/caracteristique.csv'
df = pd.read_csv(dataset, delimiter=',')

# Show the data as a table
st.write(df)




