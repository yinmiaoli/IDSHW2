#!/usr/bin/env python
# coding: utf-8

# In[65]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st
import altair as alt
import pydeck as pdk
from pydeck.types import String
import seaborn as sns
from matplotlib.figure import Figure

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")
# @st.cache

df = pd.read_csv("AB_NYC_2019.csv")
# Drop the rows where all elements are missing.
df = df.dropna()
# explore data:
# df['room_type'].value_counts()
neighbourhood = df.neighbourhood.unique()
neighbourhood_price = dict(df.groupby('neighbourhood')['price'].mean())
# neighbourhood_price_sort_top_5 = sorted(neighbourhood_price,key = neighbourhood_price.get,reverse = True)[:5]
# neighbourhood_price_sort_last_5 = sorted(neighbourhood_price,key = neighbourhood_price.get)[:5]

# print(neighbourhood_price_sort_top_5)
# print(neighbourhood_price_sort_last_5)
# print(neighbourhood_price)
room_type = dict(df['room_type'].value_counts())
# draw the map
def map(data, lat, lon, zoom):
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["longitude", "latitude"],
                auto_highlight=True,
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                coverage=1,
            ),
        ]
    ))

# laying out the map
row1_1,row1_2 = st.columns((2,3))
zoom_level = 12
midpoint = (np.average(df["latitude"]),np.average(df["longitude"]))
with row1_1:
    st.title("2019 NYC Airbnb")
    st.write("**Select a room type to see how many rooms each location contain.**")
    st.write('**Select room types:**')
    option_1 = st.checkbox('Entire home/apt')
    option_2 = st.checkbox('Private room')
    option_3 = st.checkbox('Shared room')
    if option_1 and not option_2 and not option_3:
        df = df[(df["room_type"] == 'Entire home/apt')]
    if option_2 and not option_1 and not option_3:
        df = df[(df["room_type"] == 'Private room')]
    if option_3 and not option_1 and not option_2:
        df = df[(df["room_type"] == 'Shared room')]
    if option_1 and option_2 and not option_3:
        df = df[(df["room_type"] != 'Shared room')]
    if option_1 and option_3 and not option_2:
        df = df[(df["room_type"] != 'Private room')]
    if option_2 and option_3 and not option_1:
        df = df[(df["room_type"] != 'Entire home/apt')]
    room_type = dict(df['room_type'].value_counts())
    for key, value in room_type.items():
        st.write(key, ' : ', value)
    st.write("In below diagrams, the left column shows the relationship between Price and Neighbourhood. According to your selection of room types with the checkbox, we list the top 5 expensive and the top 5 cheap neighbourhood to live in. The right columns is the map, that you could see how many rooms each location (the top 5 and the least 5) contain.")

with row1_2:
    map(df, midpoint[0],midpoint[1],12)


# get the means of the selected type
neighbourhood = df.neighbourhood.unique()
neighbourhood_price = dict(df.groupby('neighbourhood')['price'].mean())
neighbourhood_price_sort_top_5 = sorted(neighbourhood_price,key = neighbourhood_price.get,reverse = True)[:5]
neighbourhood_price_sort_last_5 = sorted(neighbourhood_price,key = neighbourhood_price.get)[:5]

global data1,data2
row2_1,row2_2 = st.columns((2,3))
with row2_1:
    st.subheader('The relationship of Price and top 5 expensive neighbourhood')
    st.write("**The top 5 expensive neighbourhood:**", ', '.join(str(value) for value in neighbourhood_price_sort_top_5))
    # get the data of the top 5 expensive neighbourhood.
    np_top_5_price = []
    for i in neighbourhood_price_sort_top_5:
        np_top_5_price.append(neighbourhood_price[i])
    fig = Figure()
    ax = fig.subplots()
    sns.barplot(x=neighbourhood_price_sort_top_5, y =np_top_5_price, ax=ax )
    ax.set_xlabel('Neighbourhood')
    ax.set_ylabel('Price')
    st.pyplot(fig)

with row2_2:
    st.subheader('The location of the top 5 expensive neighbourhood, and the number of rooms in each location')
    data1 = df[(df["neighbourhood"] == neighbourhood_price_sort_top_5[0])|(df["neighbourhood"] == neighbourhood_price_sort_top_5[1])|(df["neighbourhood"] == neighbourhood_price_sort_top_5[2])|(df["neighbourhood"] == neighbourhood_price_sort_top_5[3])|(df["neighbourhood"] == neighbourhood_price_sort_top_5[4])]
    midpoint1 = (np.average(data1["latitude"]),np.average(data1["longitude"]))
    map(data1, midpoint1[0],midpoint1[1],12)

row3_1,row3_2 = st.columns((2,3))
with row3_1:
    st.subheader('The relationship of Price and top 5 cheapest neighbourhood')
    st.write("**The top 5 cheapest neighbourhood:**", ', '.join(str(value) for value in neighbourhood_price_sort_last_5))
    # get the data of the top 5 expensive neighbourhood.
    np_cheap_5_price = []
    for i in neighbourhood_price_sort_last_5:
        np_cheap_5_price.append(neighbourhood_price[i])
    fig2 = Figure()
    ax2 = fig2.subplots()
    sns.barplot(x=neighbourhood_price_sort_last_5, y =np_cheap_5_price, ax=ax2 )
    ax2.set_xlabel('Neighbourhood')
    ax2.set_ylabel('Price')
    st.pyplot(fig2)

with row3_2:
    st.subheader('The location of the top 5 cheapest neighbourhood, and the number of rooms in each location')
    data2 = df[(df["neighbourhood"] == neighbourhood_price_sort_last_5[0])|(df["neighbourhood"] == neighbourhood_price_sort_last_5[1])|(df["neighbourhood"] == neighbourhood_price_sort_last_5[2])|(df["neighbourhood"] == neighbourhood_price_sort_last_5[3])|(df["neighbourhood"] == neighbourhood_price_sort_last_5[4])]
    midpoint2 = (np.average(data2["latitude"]),np.average(data2["longitude"]))
    map(data2, midpoint2[0],midpoint2[1],12)
