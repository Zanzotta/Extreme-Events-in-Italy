import streamlit as st
import pandas as pd
import plotly.express as px 

st.title("Italy Extreme Events Analysis")
st.write("In recent years, newspapers have increasingly reported that extreme events are becoming more frequent and severe." \
         "These events pose significant risks to our lives and communities, often resulting in widespread destruction." \
         "While a common approach to mitigating their impact is through insurance, this analysis takes a different focus.")
st.write("This analysis does not focus on insurance subscriptions. Instead, we aim to verify whether extreme events are becoming more frequent by examining the data. " \
        "Using the EM-DAT emergency events dataset, we will analyze extreme events in Italy across the 20th and 21st centuries. " \
        "To begin, we will identify the most frequently occurring types of extreme events and visualize their frequency in a bar chart")
#-------------------------#
# IMPORT DATA
#-------------------------#
italy_disaster = pd.read_csv("italy_disaster.csv")
italy_disaster['Year'] = italy_disaster['DisNo.'].str.split('-').str[0].astype(int)
plot = italy_disaster.groupby('Disaster Type').size().reset_index(name='n')
heatmap = italy_disaster.groupby(['Year', 'Disaster Type']).size().reset_index(name='Count')
heatmap_pivot = heatmap.pivot(index='Disaster Type', columns='Year', values='Count').fillna(0) 

#-------------------------#
# BOX DI SELEZIONE GRAFICO
#-------------------------#
with st.container(border=True):
    Extreme_Events = st.multiselect("Extreme events", plot['Disaster Type'], default=plot['Disaster Type'].tolist())

if Extreme_Events:
    filtered_plot = plot[plot['Disaster Type'].isin(Extreme_Events)]
else:
    filtered_plot = plot

#-------------------------#
# BAR CHART
#-------------------------#
fig = px.bar(filtered_plot.sort_values('n',ascending=True), x='n', y='Disaster Type', orientation='h', 
             labels={'n': 'Number of occurences', 'Disaster Type': ''}, color_discrete_sequence=['#E63946'])
st.plotly_chart(fig, use_container_width=True)
st.write("The podium for the most frequent extreme events in Italy goes to floods, earthquakes, and water related incidents. " \
"While floods and earthquakes are self explanatory, the water category definition is: Transport accidents involving sailing boats, ferries, cruise ships, and other vessels")

#-------------------------#
# HEATMAP
#-------------------------#
st.subheader('Extreme events over time')
st.write("To assess whether extreme events have become more frequent in recent years, we will use a heatmap. " \
"This visualization will help us identify if there is a noticeable increase in colored areas indicating higher event frequency toward the present")
fig = px.imshow(
    heatmap_pivot,
    labels=dict(x="Year", y="", color="n° of Extreme Events"),
    color_continuous_scale='Reds',
    aspect="auto")
st.plotly_chart(fig, use_container_width=True)
st.write("The data shows a noticeable increase in the occurrence of floods, water related disasters, and storms in recent years. While floods and storms are likely linked to climate change, " \
"the rise in water related disasters in Italy is largely driven by the Mediterranean migration route an issue more closely tied to humanitarian crises, such as shipwrecks, rather than environmental factors"
"While earthquakes hold a place on the podium for the most frequent extreme events in Italy historically, they do not appear among the most frequent events after 2000."\
"This suggests that earthquakes have consistently occurred in Italy, but their frequency has not increased over the past two decades")


st.subheader('Source')

st.write("The dataset can be found at: https://dataverse.uclouvain.be/dataset.xhtml?persistentId=doi:10.14428/DVN/I0LTPH or https://doc.emdat.be/")



