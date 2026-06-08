import streamlit as st
import pandas as pd
import requests
from datetime import date

st.set_page_config("Clima Yucatán", "🌿", layout="wide")

ESTACIONES = {
    "Mérida":       (20.97, -89.62),
    "Río Lagartos": (21.60, -88.16),
    "Cancún":       (21.16, -86.85),
    "Sian Ka'an":   (19.96, -87.55),
}

@st.cache_data(ttl=3600)
def cargar_clima(lat, lon, ini, fin):
    r = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={"latitude": lat, "longitude": lon,
                "start_date": str(ini), "end_date": str(fin),
                "daily": "temperature_2m_mean,precipitation_sum",
                "timezone": "America/Mexico_City"}
    )
    df = pd.DataFrame(r.json()["daily"])
    df["time"] = pd.to_datetime(df["time"])
    return df

# sidebar
estacion = st.sidebar.selectbox("Estación", ESTACIONES)
rango = st.sidebar.date_input("Período",
    (date(2020,1,1), date(2024,12,31)))

lat, lon = ESTACIONES[estacion]
df = cargar_clima(lat, lon, *rango)

# título
st.title(f"🌿 {estacion}")
st.caption(f"Fuente: Open-Meteo · {len(df)} días")

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("T° media",
   f"{df.temperature_2m_mean.mean():.1f} °C")
c2.metric("Lluvia total",
   f"{df.precipitation_sum.sum():.0f} mm")
c3.metric("Días sin lluvia",
   int((df.precipitation_sum == 0).sum()))

# gráfico + mapa lado a lado
g, m = st.columns([2, 1])
g.line_chart(df, x="time", y="temperature_2m_mean")
m.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))

st.dataframe(df, use_container_width=True, hide_index=True)