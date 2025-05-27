import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Predicción de Delitos en Lima", layout="wide")
st.title("Predicción de Incidencias Delictivas en Lima Metropolitana")
st.markdown("Análisis basado en datos históricos del año 2023")

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("delitos_denunciados_2023_0.csv")

df = cargar_datos()

# Preprocesamiento básico
df["FECHA_HECHO"] = pd.to_datetime(df["FECHA_HECHO"], errors="coerce")
df["AÑO"] = df["FECHA_HECHO"].dt.year
df["MES"] = df["FECHA_HECHO"].dt.month
df = df.dropna(subset=["FECHA_HECHO", "MES"])

# Selección de distrito y tipo de delito
distritos = sorted(df["DISTRITO"].dropna().unique())
delitos = sorted(df["DELITO"].dropna().unique())

col1, col2 = st.columns(2)
with col1:
    distrito_sel = st.selectbox("Selecciona un distrito", distritos)
with col2:
    delito_sel = st.selectbox("Selecciona un tipo de delito", delitos)

# Filtrar datos
filtro = df[(df["DISTRITO"] == distrito_sel) & (df["DELITO"] == delito_sel)]

# Mostrar estadísticas
st.subheader(f"Estadísticas en {distrito_sel} para {delito_sel}")
st.write(f"Total de casos registrados: {len(filtro)}")

# Visualización histórica mensual
conteo_mensual = filtro.groupby("MES").size().reindex(range(1, 13), fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(x=conteo_mensual.index, y=conteo_mensual.values, marker='o', ax=ax)
ax.set_title("Casos Mensuales en 2023")
ax.set_xlabel("Mes")
ax.set_ylabel("Número de Casos")
st.pyplot(fig)

# Modelo predictivo simple para 2025
X = conteo_mensual.index.values.reshape(-1, 1)
y = conteo_mensual.values
modelo = LinearRegression().fit(X, y)
meses_2025 = np.array(range(1, 13)).reshape(-1, 1)
predicciones = modelo.predict(meses_2025).round().astype(int)
predicciones = np.clip(predicciones, a_min=0, a_max=None)

# Mostrar predicción
st.subheader("Proyección de casos para 2025")
df_pred = pd.DataFrame({
    "Mes": range(1, 13),
    "Casos estimados": predicciones
})
st.dataframe(df_pred.set_index("Mes"))

# Visualización de predicción
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(x=df_pred["Mes"], y=df_pred["Casos estimados"], palette="Reds", ax=ax2)
ax2.set_title("Predicción mensual de delitos en 2025")
ax2.set_xlabel("Mes")
ax2.set_ylabel("Casos Estimados")
st.pyplot(fig2)

st.info("Esta es una herramienta predictiva basada en datos históricos. Para usos oficiales, se recomienda validar con entidades correspondientes.")
