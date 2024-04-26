# %%writefile $app_file

######################
# Import libraries
######################

import pandas as pd
import streamlit as st
from PIL import Image

import math
from datetime import datetime

import pandas as pd

import plotly.express as px
import folium
from streamlit_folium import folium_static


######################
# Page Title
######################

# PIL.Image
image = Image.open('ft-logo.png')

#https://docs.streamlit.io/library/api-reference/media/st.image
st.image(image, use_column_width=True)

st.write('The purpose of this webapp is to allow you to search for options of homes in your selected area.')


@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()

st.header('AireBnB Data NYC (2019-09-12)')
st.dataframe(df.head(10))

st_group = st.selectbox('NYC boroughs', df['neighbourhood_group'].unique())
a = df[df['neighbourhood_group']==st_group]
st_select_group = st.multiselect('select your neighbourhoods', a['neighbourhood'].unique(), default=a['neighbourhood'].unique()[0])
b = df[df['neighbourhood'].isin(st_select_group)]
st.dataframe(b.head())

st.subheader('Selecting a subset of columns')

st.write("---")

values = st.slider("Price range", float(b.price.min()), float(b.price.max()), (float(b.price.min()), float(b.price.max())))
c = b[b.price.between(values[0],values[1])]
# st.write(c)
st.write(f'Total {len(c)} housing rentals are found in {st_select_group} {st_group} with price between \${values[0]} and \${values[1]}')

# Get "latitude", "longitude", "price" for top listings
toplistings = df.query("price>=800")[["name", "latitude", "longitude", "price"]].dropna(how="any").sort_values("price", ascending=False)

Top = toplistings.values[0,:]
m = folium.Map(location=Top[1:-1], zoom_start=16)

tooltip = "Top listings"
for j in range(len(c)):
    name, lat, lon, price, neighbourhood, host_name, room_type = c[['name', 'latitude', 'longitude', 'price', 'neighbourhood', 'host_name', 'room_type']].values[j,:]
    folium.Marker(
            (lat,lon), popup=f"{name}" , tooltip=f"Name:{name}<br> Neighbourhood:{neighbourhood}<br> Host name:{host_name}<br> Room type:{room_type}<br> Price:${price}"
        ).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)
