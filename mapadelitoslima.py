import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

st.set_page_config(page_title="Predicción de Delitos - Lima", layout="wide")
st.title("Análisis y Predicción de Delitos en Lima Metropolitana (Perú)")

# Cargar CSV
uploaded_file = st.file_uploader("Sube el archivo CSV de delitos", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Mostrar columnas disponibles
    st.subheader("Columnas detectadas en el archivo:")
    st.write(df.columns.tolist())

    # Intentar encontrar columna de fecha automáticamente
    posibles_fechas = [col for col in df.columns if "fecha" in col.lower()]
    if posibles_fechas:
        fecha_col = posibles_fechas[0]
        st.success(f"Usando la columna de fecha: {fecha_col}")
        df[fecha_col] = pd.to_datetime(df[fecha_col], errors="coerce")
        df = df.dropna(subset=[fecha_col])
        df["AÑO"] = df[fecha_col].dt.year
        df["MES"] = df[fecha_col].dt.month
    else:
        st.error("No se encontró una columna de fecha válida.")
        st.stop()

    # Estadísticas simples
    st.subheader("Estadísticas generales")
    st.write("Total de delitos registrados:", len(df))
    st.write("Años cubiertos:", df["AÑO"].unique())

    # Gráfico por mes
    st.subheader("Distribución de delitos por mes")
    delitos_por_mes = df.groupby("MES").size()
    fig, ax = plt.subplots()
    ax.plot(delitos_por_mes.index, delitos_por_mes.values, marker="o")
    ax.set_title("Delitos por mes")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Número de delitos")
    st.pyplot(fig)

    # Modelo predictivo simple por mes
    st.subheader("Predicción simple de delitos por mes")
    X = np.array(df["MES"]).reshape(-1, 1)
    y = df.groupby("MES").size().values
    y = y[:len(X)]  # Alinear dimensiones

    modelo = LinearRegression()
    modelo.fit(X, y)
    predicciones = modelo.predict(X)

    fig2, ax2 = plt.subplots()
    ax2.scatter(X, y, label="Histórico", color="blue")
    ax2.plot(X, predicciones, label="Predicción", color="red")
    ax2.set_title("Predicción de delitos por mes")
    ax2.set_xlabel("Mes")
    ax2.set_ylabel("Casos")
    ax2.legend()
    st.pyplot(fig2)

    # Información de predicción
    st.info("Este modelo usa regresión lineal simple con base en los datos históricos cargados. Para una predicción real a futuro, se puede integrar modelos avanzados con más variables.")
else:
    st.warning("Por favor, sube un archivo CSV válido para comenzar el análisis.")
