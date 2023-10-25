import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt

import altair as alt
st.set_page_config(
    layout="wide")
# Title and header
st.title("Dashboard conteo clientes por tipo - Prueba técnica Joaquín Avendaño")
st.header('Total de clientes por concesionaria y tipo')

data = pd.read_excel("clientes_libres.xlsx", skiprows=3)
data2= pd.read_excel("clientes_libres.xlsx", skiprows=3)
data_conteo=pd.read_excel("conteo_clientes.xlsx")
# Forward-fill the missing "TIPO_CLIENTE" values
data_conteo['TIPO_CLIENTE'].fillna(method='ffill', inplace=True)

# Filter out the rows where "TIPO_CLIENTE" is 'TIPO_CLIENTE'
data_conteo = data_conteo[data_conteo['TIPO_CLIENTE'] != 'TIPO_CLIENTE']


# Forward-fill the missing "TIPO_CLIENTE" values
data_conteo['CONCESIONARIA'].fillna(method='ffill', inplace=True)

# Filter out the rows where "TIPO_CLIENTE" is 'TIPO_CLIENTE'
data_conteo = data_conteo[data_conteo['CONCESIONARIA'] != 'CONCESIONARIA']
# Define the mapping dictionary for replacement
replace_dict = {'L': 'Libre', 'PL': 'Potencialmente Libre', 'R': 'Regulado'}

# Replace values in the 'TIPO_CLIENTE' column
data_conteo['TIPO_CLIENTE'] = data_conteo['TIPO_CLIENTE'].replace(replace_dict)
# Define the new column names
new_column_names = ['Concesionaria', 'Tipo Cliente', 'Total Clientes']

# Assign the new column names to the DataFrame
data_conteo.columns = new_column_names
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.title()
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.replace('Enel_Distribucion', 'Enel Distribucion')
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.replace('Eepa', 'EEPA')

data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.replace('sa', 'SA').str.replace('s.a', 'S.A')
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.replace('CaSAblanca', 'Casablanca')

regulado=data_conteo[data_conteo["Tipo Cliente"]=='Regulado']
pl=data_conteo[data_conteo["Tipo Cliente"]=='Potencialmente Libre']
libre=data_conteo[data_conteo["Tipo Cliente"]=='Libre']

# Sort the data by 'Total Clientes' in descending order

# Sort the data by 'Total Clientes' in descending order
regulado = regulado.sort_values(by='Total Clientes', ascending=False)
pl = pl.sort_values(by='Total Clientes', ascending=False)
libre = libre.sort_values(by='Total Clientes', ascending=False)

col1, col2,col3 = st.columns(3)

# Create a Streamlit app

# Create a horizontal bar chart with selection
selection = alt.selection_multi(fields=['Concesionaria'], bind='legend')

chart = alt.Chart(regulado).mark_bar().encode(
    x=alt.X('Total Clientes:Q', axis=alt.Axis(title='Total Clientes')),
    y=alt.Y('Concesionaria:N', sort='-x', axis=alt.Axis(title='Concesionaria')),
    color=alt.condition(selection, alt.ColorValue('steelblue'), alt.ColorValue('lightgray'))
).properties(
    title='Total Clientes Regulados',
    width=700,
    height=400
).add_selection(selection)

chart2 = alt.Chart(pl).mark_bar().encode(
    x=alt.X('Total Clientes:Q', axis=alt.Axis(title='Total Clientes')),
    y=alt.Y('Concesionaria:N', sort='-x', axis=alt.Axis(title='Concesionaria')),
    color=alt.condition(selection, alt.ColorValue('steelblue'), alt.ColorValue('lightgray'))
).properties(
    title='Total Clientes Potencialmente libres',
    width=700,
    height=400
).add_selection(selection)

chart3 = alt.Chart(libre).mark_bar().encode(
    x=alt.X('Total Clientes:Q', axis=alt.Axis(title='Total Clientes')),
    y=alt.Y('Concesionaria:N', sort='-x', axis=alt.Axis(title='Concesionaria')),
    color=alt.condition(selection, alt.ColorValue('steelblue'), alt.ColorValue('lightgray'))
).properties(
    title='Total Clientes Libres',  # Add a title
    width=700,
    height=400
).add_selection(selection)
# Display the chart in Streamlit
with col1:
    st.altair_chart(chart, use_container_width=True)
with col2:
    st.altair_chart(chart2, use_container_width=True)
with col3:
    st.altair_chart(chart3, use_container_width=True)
st.caption("Fuente: Resumen de excel consolidado", unsafe_allow_html=False)