import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression

import altair as alt

## Establecer configuración de la página
st.set_page_config(
    layout="wide")

#Titulo y primera impresión
st.title("Dashboard conteo clientes por tipo - Prueba técnica Joaquín Avendaño")
st.header('Total de clientes por concesionaria y tipo')


## Carga de la data
data = pd.read_excel("clientes_regulados_osorno.xlsx", skiprows=3)
data2= pd.read_excel("clientes_libres.xlsx", skiprows=3)
data_conteo=pd.read_excel("conteo_clientes.xlsx")

### Procesamiento de los strings de la data para hacerlo más presentable
data_conteo['TIPO_CLIENTE'].fillna(method='ffill', inplace=True)
data_conteo = data_conteo[data_conteo['TIPO_CLIENTE'] != 'TIPO_CLIENTE']
data_conteo['CONCESIONARIA'].fillna(method='ffill', inplace=True)
data_conteo = data_conteo[data_conteo['CONCESIONARIA'] != 'CONCESIONARIA']
replace_dict = {'L': 'Libre', 'PL': 'Potencialmente Libre', 'R': 'Regulado'}
data_conteo['TIPO_CLIENTE'] = data_conteo['TIPO_CLIENTE'].replace(replace_dict)
new_column_names = ['Concesionaria', 'Tipo Cliente', 'Total Clientes']
data_conteo.columns = new_column_names
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.title()
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.replace('Enel_Distribucion', 'Enel Distribucion')
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.replace('Eepa', 'EEPA')
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.replace('sa', 'SA').str.replace('s.a', 'S.A')
data_conteo['Concesionaria'] = data_conteo['Concesionaria'].str.replace('CaSAblanca', 'Casablanca')

## Filtrado para gráficos
regulado=data_conteo[data_conteo["Tipo Cliente"]=='Regulado']
pl=data_conteo[data_conteo["Tipo Cliente"]=='Potencialmente Libre']
libre=data_conteo[data_conteo["Tipo Cliente"]=='Libre']

#Orden de los datos
regulado = regulado.sort_values(by='Total Clientes', ascending=False)
pl = pl.sort_values(by='Total Clientes', ascending=False)
libre = libre.sort_values(by='Total Clientes', ascending=False)

col1, col2,col3 = st.columns(3)
selection = alt.selection_multi(fields=['Concesionaria'], bind='legend')

### Creación de los gráficos
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


#Función de streamlit para dividir en columnas:
with col1:
    st.altair_chart(chart, use_container_width=True)
with col2:
    st.altair_chart(chart2, use_container_width=True)
with col3:
    st.altair_chart(chart3, use_container_width=True)
st.caption("Fuente: Resumen de excel consolidado", unsafe_allow_html=False)

#Tabla expandible con origen de los datos
with st.expander("Expandir para ver detalle:"):
    c1, c2,c3 = st.columns(3)

    data_conteo.sort_values(by=["Tipo Cliente","Total Clientes"], ascending=False, inplace=True)
    with c1:
        st.dataframe(regulado, use_container_width=False)
    with c2:
        st.dataframe(pl, use_container_width=False)
    with c3:
        st.dataframe(libre, use_container_width=False)

st.header('Clientes regulares que pueden ser evaluados para pasar a libres, según su consumo:')

st.subheader("Metodología: ")
st.write("Para encontrar clientes que de momento son regulados, pero tienen potencial de libres, esto se logra mediante un modelo de clasificación entre clientes libres y regulados el consumo promedio de los últimos 12 meses en kWh.")
st.write("El modelo de clasificación lo que hace básicamente es asignarle una etiqueta según las variables dependientes que le entreguemos, en este caso, el consumo promedio de los últimos 12 meses en kWh, no obstante, un modelo más avanzado puede tomar más variables.")

st.write("Dado lo anterior, se tomarán desde las predicciones los 5 clientes regulados con el consumo más alto, que podrían pasar a la categoría de libres y que correspondan a la concesionaria de Compañía Eléctrica de Osorno. En otras palabras, aquellos que el modelo predijo que deberían ser libres, pero en este momento se encuentran bajo la tarifa regulada.")

#Data corresponde a la lista de los clientes regulados de osorno.

#data2 corresponde a la lista de los clientes libres a lo largo de Chile.

#Procesamiento de los datos nuevamente, pero para detectar clientes
data['TIPO_CLIENTE'].fillna(method='ffill', inplace=True)
data = data[data['TIPO_CLIENTE'] != 'TIPO_CLIENTE']
data['CONCESIONARIA'].fillna(method='ffill', inplace=True)
data = data[data['CONCESIONARIA'] != 'CONCESIONARIA']
data2['TIPO_CLIENTE'].fillna(method='ffill', inplace=True)
data2 = data2[data2['TIPO_CLIENTE'] != 'TIPO_CLIENTE']
data2['CONCESIONARIA'].fillna(method='ffill', inplace=True)
data2 = data2[data2['CONCESIONARIA'] != 'CONCESIONARIA']
data=data.drop(columns=['RUT CLIENTE', 'ALIMENTADOR', 'TENSIÓN DE CONEXIÓN [V]'])
data2=data2.drop(columns=['RUT CLIENTE', 'ALIMENTADOR', 'TENSIÓN DE CONEXIÓN [V]'])
data = data[data['CONSUMO PROMEDIO ÚLTIMOS 12 MESES [kWh]'] != '(en blanco)']
data = data[data['S/E PRIMARIA'] != '(en blanco)']
data = data[data['CLIENTE_ID'] != '(en blanco)']
data = data[data['NOMBRE O RAZÓN SOCIAL DEL CLIENTE'] != '(en blanco)']
data = data[data['TIPO_EMPALME_ID'] != '(en blanco)']
data = data[data['POTENCIA_CONECTADA [kW]'] != '(en blanco)']
data2 = data2[data2['CONSUMO PROMEDIO ÚLTIMOS 12 MESES [kWh]'] != '(en blanco)']
data2 = data2[data2['S/E PRIMARIA'] != '(en blanco)']
data2 = data2[data2['CLIENTE_ID'] != '(en blanco)']
data2 = data2[data2['NOMBRE O RAZÓN SOCIAL DEL CLIENTE'] != '(en blanco)']
data2 = data2[data2['TIPO_EMPALME_ID'] != '(en blanco)']
data2 = data2[data2['POTENCIA_CONECTADA [kW]'] != '(en blanco)']
#Eliminar datos con ausentes
data.dropna(inplace=True)
#Unir las bases de clientes regulados y libres
df_merged = pd.concat([data, data2], ignore_index=True, sort=False)
df_merged.dropna(inplace=True)
df=df_merged.copy()

### Entrenamiento del modelo
le = LabelEncoder()
df['TIPO_CLIENTE'] = le.fit_transform(df['TIPO_CLIENTE'])
X = df[['CONSUMO PROMEDIO ÚLTIMOS 12 MESES [kWh]']]
Y = df['TIPO_CLIENTE']

#Separación base de datos para validación de resultados
X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=20)
class_weights = {0: 10.0, 1: 1.0}  
logistic_model = LogisticRegression(solver='lbfgs', max_iter=1000, class_weight=class_weights, random_state=20)
logistic_model.fit(X_train, y_train)
pred = logistic_model.predict(X_val)
results = pd.DataFrame({'Actual': y_val, 'Predicted': pred})
results['Classification Error'] = (results['Actual'] != results['Predicted'])
misclassified_clients = results[results['Classification Error'] == True]
#misclassified_clients[(misclassified_clients["Actual"]==1) & (misclassified_clients["Predicted"]==0)]

