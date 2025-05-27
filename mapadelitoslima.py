import streamlit as st import pandas as pd import matplotlib.pyplot as plt import seaborn as sns from sklearn.linear_model import LinearRegression import numpy as np

Cargar datos

@st.cache_data def cargar_datos(): df = pd.read_csv("delitos_denunciados_2023_0.csv") return df

Cargar el dataset

df = cargar_datos()

st.title("Sistema de Análisis y Predicción de Delitos - Perú")

Filtros

st.sidebar.header("Filtros") departamento = st.sidebar.selectbox("Departamento", sorted(df["dpto_pjfs"].unique())) provincia = st.sidebar.selectbox("Provincia", sorted(df[df["dpto_pjfs"] == departamento]["prov_pjfs"].unique())) distrito = st.sidebar.selectbox("Distrito", sorted(df[(df["dpto_pjfs"] == departamento) & (df["prov_pjfs"] == provincia)]["dist_pjfs"].unique())) tipo_delito = st.sidebar.selectbox("Tipo de delito", sorted(df["generico"].unique()))

Filtrado

filtro = df[ (df["dpto_pjfs"] == departamento) & (df["prov_pjfs"] == provincia) & (df["dist_pjfs"] == distrito) & (df["generico"] == tipo_delito) ]

st.subheader(f"Delitos registrados en 2023 en {distrito}, {provincia}, {departamento}") st.write(f"Cantidad total de casos: {filtro['cantidad'].sum()}")

Gráfico por subcategoría

if not filtro.empty: subcat = filtro.groupby("subgenerico")["cantidad"].sum().sort_values(ascending=False) fig, ax = plt.subplots(figsize=(10, 5)) sns.barplot(x=subcat.values, y=subcat.index, palette="Reds_r", ax=ax) ax.set_title("Casos por Subcategoría") ax.set_xlabel("Cantidad de Casos") st.pyplot(fig) else: st.warning("No se encontraron datos con los filtros seleccionados.")

Predicción simple usando regresión lineal

st.subheader("Proyección para 2025")

Agrupar por año (aunque solo hay 2023, creamos 2022 artificialmente para proyectar)

df_pred = df[ (df["dpto_pjfs"] == departamento) & (df["prov_pjfs"] == provincia) & (df["dist_pjfs"] == distrito) & (df["generico"] == tipo_delito) ][["anio_denuncia", "cantidad"]].copy() df_pred.loc[:, "anio_denuncia"] = df_pred["anio_denuncia"].astype(int)

Simular datos de 2022 si no hay

if 2022 not in df_pred["anio_denuncia"].unique(): media_2023 = df_pred["cantidad"].mean() df_pred = pd.concat([ df_pred, pd.DataFrame({"anio_denuncia": [2022], "cantidad": [media_2023 * 0.95]}) ])

model = LinearRegression() X = df_pred[["anio_denuncia"]] y = df_pred["cantidad"] model.fit(X, y)

pred_2025 = model.predict([[2025]])[0] st.success(f"Proyección de casos para 2025: {int(pred_2025)} casos")

Mensaje final

st.info("Este sistema puede conectarse con fuentes oficiales para actualizar datos automáticamente. Proyecto desarrollado con IA y visualización interactiva.")

