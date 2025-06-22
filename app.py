import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Dashboard Electoral", layout="wide")

st.title("📊 Dashboard Electoral Interactivo")
st.markdown("Visualización interactiva de datos electorales por candidato y región.")

# --- Cargar datos ---
@st.cache_data
def load_data():
    return pd.read_csv("datos_elecciones.csv")

df = load_data()

# --- Filtro por Región ---
regiones = df['Región'].unique().tolist()
region_seleccionada = st.sidebar.selectbox("🔍 Filtrar por Región", options=["Todas"] + regiones)

if region_seleccionada != "Todas":
    df = df[df['Región'] == region_seleccionada]

# --- Agrupar pestañas por temática ---
tab1, tab2, tab3 = st.tabs(["📍 Métricas Clave", "💬 Sentimiento", "⭐ Score y Volumen"])

# --- TAB 1: Métricas Clave ---
with tab1:
    st.subheader("📌 Regiones Ganadas por Candidato")
    regiones_ganadas = df.groupby('Candidato')['Ganador'].sum().reset_index()
    fig1 = px.bar(regiones_ganadas, x='Ganador', y='Candidato', orientation='h',
                  color='Candidato', title="Número de Regiones Ganadas")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🎯 Probabilidad de Victoria")
    fig2 = px.bar(df, x='Candidato', y='Probabilidad', color='Candidato',
                  title="Probabilidad de Victoria por Candidato", hover_data=['Región'])
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 2: Sentimiento ---
with tab2:
    st.subheader("💬 Sentimiento Promedio por Candidato")
    sentimiento_prom = df.groupby('Candidato')['Sentimiento'].mean().reset_index().sort_values(by='Sentimiento', ascending=False)
    fig3 = px.bar(sentimiento_prom, x='Candidato', y='Sentimiento', color='Sentimiento',
                  color_continuous_scale='Viridis', title="Sentimiento Promedio")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📈 Distribución del Sentimiento Total (%)")
    sentimiento_porcentaje = (df.groupby('Candidato')['Sentimiento'].sum() / df['Sentimiento'].sum() * 100).reset_index()
    sentimiento_porcentaje.columns = ['Candidato', 'Sentimiento (%)']
    fig4 = px.pie(sentimiento_porcentaje, names='Candidato', values='Sentimiento (%)',
                  title="Porcentaje del Sentimiento Total por Candidato")
    st.plotly_chart(fig4, use_container_width=True)

# --- TAB 3: Score y Volumen ---
with tab3:
    st.subheader("📌 Score Promedio por Candidato")
    scores = df.groupby('Candidato')['Score'].mean().reset_index()
    fig5 = px.line(scores, x='Candidato', y='Score', markers=True, text=scores['Score'].round(2),
                   title="Score Promedio por Candidato")
    fig5.update_traces(textposition='top center')
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("📊 Volumen Normalizado por Candidato")
    fig6 = px.bar(df, y='Candidato', x='Volumen_Norm', color='Candidato', orientation='h',
                  title="Volumen Normalizado por Candidato")
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("📉 Fuerza Histórica por Candidato")
    fuerza = df.groupby('Candidato')['Fuerza_Histórica'].mean().reset_index()
    fig7 = px.line(fuerza, x='Candidato', y='Fuerza_Histórica', markers=True,
                   title="Fuerza Histórica de los Candidatos")
    st.plotly_chart(fig7, use_container_width=True)
