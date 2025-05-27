import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
import folium
from streamlit_folium import st_folium

# Cargar los datos
df = pd.read_csv("delitos_denunciados_2023_0.csv")

# Limpieza y renombre
df.columns = df.columns.str.lower()
df = df.rename(columns={
    'anio_denuncia': 'anio',
    'dpto_pjfs': 'departamento',
    'prov_pjfs': 'provincia',
    'dist_pjfs': 'distrito',
    'generico': 'categoria',
    'cantidad': 'casos'
})
df['casos'] = pd.to_numeric(df['casos'], errors='coerce')
df = df.dropna(subset=['casos'])

# Interfaz
st.title("Mapa Interactivo y Predicción de Delitos en Perú")

# Filtros
departamento = st.selectbox("Selecciona el departamento", sorted(df['departamento'].dropna().unique()))
categoria = st.selectbox("Selecciona el tipo de delito", sorted(df['categoria'].dropna().unique()))

filtro_df = df[(df['departamento'] == departamento) & (df['categoria'] == categoria)]

# Estadísticas
st.subheader("Estadísticas por distrito")
casos_distrito = filtro_df.groupby('distrito')['casos'].sum().sort_values(ascending=False)
st.bar_chart(casos_distrito)

# Mapa simulado
st.subheader("Mapa de incidencia delictiva (simulado)")
mapa = folium.Map(location=[-12.0464, -77.0428], zoom_start=11)

for i, (distrito, casos) in enumerate(casos_distrito.items()):
    folium.CircleMarker(
        location=[-12.05 + i*0.01, -77.05 + i*0.01],
        radius=min(casos / 50, 15),
        popup=f"{distrito}: {int(casos)} casos",
        color="red",
        fill=True,
        fill_opacity=0.6
    ).add_to(mapa)

st_folium(mapa, width=700, height=500)

# Predicción
st.subheader("Proyección delictiva")
pred_df = filtro_df.groupby('anio')['casos'].sum().reset_index()
if len(pred_df) > 1:
    X = pred_df['anio'].values.reshape(-1, 1)
    y = pred_df['casos'].values
    modelo = LinearRegression().fit(X, y)
    futuro = np.array([2024, 2025]).reshape(-1, 1)
    pred = modelo.predict(futuro)

    fig, ax = plt.subplots()
    sns.barplot(x=pred_df['anio'], y=pred_df['casos'], ax=ax)
    ax.plot(futuro.flatten(), pred, color='red', linestyle='--', marker='o', label="Predicción")
    ax.set_title("Tendencia de casos delictivos")
    ax.legend()
    st.pyplot(fig)

    st.success(f"Proyección para 2025: {int(pred[-1])} casos estimados en {departamento} para '{categoria}'")
else:
    st.warning("No hay suficientes datos para realizar una predicción.")

st.caption("Datos: CSV de delitos 2023 | Demo para uso público y gubernamental")
