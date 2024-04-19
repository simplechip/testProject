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
st_select_group = st.multiselect('select your neighbourhoods', a['neighbourhood'].unique())
b = df[df['neighbourhood'].isin(st_select_group)]
st.dataframe(b.head())

st.subheader('Selecting a subset of columns')

st.write("---")

values = st.slider("Price range", float(df.price.min()), 1000., (50., 300.))
st.write(f'Total {len(b)} housing rentals are found in {st_select_group} {st_group} with price between \${b.price.min()} and \${b.price.max()}')

st.write("---")

st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")

# Get "latitude", "longitude", "price" for top listings
toplistings = df.query("price>=800")[["name", "latitude", "longitude", "price"]].dropna(how="any").sort_values("price", ascending=False)

Top = toplistings.values[0,:]
m = folium.Map(location=Top[1:-1], zoom_start=16)

tooltip = "Top listings"
for j in range(50):
    name, lat, lon, price, neighbourhood, host_name, room_type = df[['name', 'latitude', 'longitude', 'price', 'neighbourhood', 'host_name', 'room_type']].values[j,:]
    folium.Marker(
            (lat,lon), popup=f"{name}" , tooltip=f"Name:{name}<br> Neighbourhood:{neighbourhood}<br> Host name:{host_name}<br> Room type:{room_type}<br> Price:${price}"
        ).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)


st.write("---")

st.markdown("""### Images and dropdowns

Use [st.image](https://streamlit.io/docs/api.html#streamlit.image) to show images of cats, puppies, feature importance plots, tagged video frames, and so on.

Now for a bit of fun.""")

pics = {
    "Cat": "https://cdn.pixabay.com/photo/2016/09/24/22/20/cat-1692702_960_720.jpg",
    "Puppy": "https://cdn.pixabay.com/photo/2019/03/15/19/19/puppy-4057786_960_720.jpg",
    "Sci-fi city": "https://storage.needpix.com/rsynced_images/science-fiction-2971848_1280.jpg",
    "Cheetah": "img/running-cheetah.jpeg",
    "FT-Logo": "ft-logo.png"
}
pic = st.selectbox("Picture choices", list(pics.keys()), 0)
st.image(pics[pic], use_column_width=True, caption=pics[pic])

st.write("---")

select_col = st.selectbox("Select Columns", list(df.columns), 0)
st.write(f"Your selection is {select_col}")
