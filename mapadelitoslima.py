import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# Título de la app
st.set_page_config(page_title="Mapa Delictivo Lima", layout="centered")
st.title("Mapa de Incidencias Delictivas - Lima Metropolitana")

# Lista de distritos
distritos = [
    "Miraflores", "San Isidro", "San Borja", "La Molina", "Santiago de Surco",
    "San Juan de Lurigancho", "Comas", "Villa El Salvador", "Ate", "Los Olivos", "San Martín de Porres"
]

# Tipos de delito simulados
tipos_delito = ["Robo", "Asalto", "Vandalismo", "Homicidio", "Microcomercialización"]

# Filtros del usuario
distrito = st.selectbox("Selecciona el distrito", distritos)
delito = st.selectbox("Selecciona el tipo de delito", tipos_delito)

# Simulación de datos (reemplazable por fuente oficial)
datos = pd.DataFrame({
    "lat": [-12.120, -12.119, -12.089, -12.071, -12.088],
    "lon": [-77.030, -77.034, -77.025, -77.040, -77.038],
    "tipo": ["Robo", "Asalto", "Robo", "Vandalismo", "Homicidio"],
    "distrito": ["Miraflores", "San Isidro", "San Isidro", "Miraflores", "San Isidro"],
    "fecha": [datetime(2025, 5, 20), datetime(2025, 5, 21), datetime(2025, 5, 22), datetime(2025, 5, 25), datetime(2025, 5, 26)]
})

# Filtrar según selección
filtro = datos[(datos["distrito"] == distrito) & (datos["tipo"] == delito)]

# Mostrar estadísticas
st.subheader("Estadísticas Simuladas")
st.write(f"Casos reportados: {len(filtro)}")
if not filtro.empty:
    st.write(f"Último caso reportado: {filtro['fecha'].max().strftime('%d/%m/%Y')}")
else:
    st.write("No se encontraron casos reportados con esos filtros.")

# Crear y mostrar el mapa
st.subheader("Mapa de Incidentes")
mapa = folium.Map(location=[-12.1, -77.03], zoom_start=12)

for _, row in filtro.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"{row['tipo']} - {row['fecha'].strftime('%d/%m/%Y')}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(mapa)

st_folium(mapa, width=700, height=500)

# Nota final
st.info("Este es un prototipo con datos simulados. Puede integrarse con fuentes oficiales como el MININTER o el INEI.")
