import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Configurar página
st.set_page_config(
    page_title="Datatools Demo",
    page_icon="📘",
    layout="wide"
)

# Estilos personalizados
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #005ca9;
    background-image: none;
}
h1, h2, h3, label, .stButton>button {
    color: #ffffff !important;
    text-shadow: 1px 1px 2px #000000;
}
.stMarkdown {
    background-color: rgba(0,0,0,0.6);
    padding: 1rem;
    border-radius: 0.5rem;
}
.stForm {
    background-color: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 1rem;
    backdrop-filter: blur(2px);
}
.stSelectbox, .stNumberInput input {
    background-color: rgba(255,255,255,0.1) !important;
    color: #ffffff !important;
    border: none;
}
[data-testid="stSlider"] .st-cq {
    background: linear-gradient(to right, #005ca9, #005ca9) !important;
}
[data-testid="stSlider"] .st-cr {
    color: #ffffff !important;
}
.stButton>button {
    background-color: #005ca9 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 0.3rem;
    padding: 0.5rem 1rem;
    border: none;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Logo institucional
st.image("assets/Logo_UFV.jpg", width=650)


# Ruta relativa segura al dataset
base_path = Path(__file__).resolve().parent.parent
csv_path = base_path / "data" / "dataset_estudiantes.csv"

# prueba confirmatoria de path
# print("Ruta al CSV:", csv_path)
# print("¿Existe el archivo?:", csv_path.exists())

# Mostrar pruebas en Streamlit
# st.write("Ruta al CSV:", csv_path)
# st.write("¿Existe el archivo?:", csv_path.exists())

# Cargar el dataset
df = pd.read_csv(csv_path)
df["Nota Media"] = (df["Nota Primer Semestre"] +
                    df["Nota Segundo Semestre"]) / 2

# Extraer opciones únicas para los campos desplegables
opciones_grado = sorted(df["Grado"].dropna().unique())
opciones_facultad = sorted(df["Facultad"].dropna().unique())
opciones_nacionalidad = sorted(df["Nacionalidad"].dropna().unique())
opciones_curso = sorted(df["Curso"].dropna().unique())
opciones_acceso = sorted(df["Tipo de Acceso"].dropna().unique())
opciones_beca = sorted(df["Beca"].dropna().unique())
opciones_abandono = sorted(df["Abandono"].dropna().unique())
opciones_sexo = sorted(df["Sexo"].dropna().unique())

# Pestañas
tab1, tab2 = st.tabs(["Predicción", "Visualización de Datos"])

with tab1:
    st.title("Datatools Predicción de Nota Media")
    st.markdown("""
    Esta demo utiliza aprendizaje automático para estimar la nota media de un estudiante  
    según sus hábitos académicos, perfil emocional y contexto institucional.
    """)

    with st.form("formulario_prediccion"):
        st.subheader("Datos del estudiante")

        edad = st.slider("Edad", 17, 30, value=18)
        asignaturas = st.number_input(
            "Asignaturas matriculadas", 1, 15, value=6)
        porcentaje = st.slider(
            "Porcentaje de Exámenes Aprobados", 0.0, 1.0, value=0.5)
        asistencia = st.slider("Asistencia", 0.0, 1.0, value=0.5)
        biblioteca = st.selectbox(
            "Visitas a Biblioteca por mes", list(range(0, 16)), index=4)
        emocional = st.slider(
            "Estado Emocional (1 = Inestable, 5 = Estable)", 1, 5, value=3)

        curso = st.selectbox("Curso", opciones_curso)
        grado = st.selectbox("Grado", opciones_grado)
        facultad = st.selectbox("Facultad", opciones_facultad)
        sexo = st.selectbox("Sexo", opciones_sexo)
        nacionalidad = st.selectbox("Nacionalidad", opciones_nacionalidad)
        acceso = st.selectbox("Tipo de Acceso", opciones_acceso)
        beca = st.selectbox("Beca", opciones_beca)
        abandono = st.selectbox("Abandono", opciones_abandono)

        enviado = st.form_submit_button("Estimar Nota Media")

    if enviado:
        url = "http://localhost:8000/predecir"  # para no docker
        # url = "http://fastapi:8000/predecir"   #para docker

        datos = {
            "Edad": edad,
            "Asignaturas": asignaturas,
            "Porcentaje_Exámenes_Aprobados": porcentaje,
            "Asistencia": asistencia,
            "Uso_Biblioteca": biblioteca,
            "Estado_Emocional": emocional,
            "Curso": curso,
            "Grado": grado,
            "Facultad": facultad,
            "Sexo": sexo,
            "Nacionalidad": nacionalidad,
            "Tipo_de_Acceso": acceso,
            "Beca": beca,
            "Abandono": abandono
        }

        try:
            respuesta = requests.post(url, json=datos)
            if respuesta.status_code == 200:
                nota = respuesta.json()["Nota Media Estimada"]
                st.success(f"Nota Media Estimada: {nota}")
            else:
                st.error("Error al conectar con la API.")
        except Exception as e:
            st.error(f"Conexión fallida: {e}")

with tab2:
    st.subheader("Análisis del Dataset Correlacionado")

    # Crear columnas para centrar el contenido
    col1, col2, col3 = st.columns([1, 2, 1])  # proporciones ajustables
    with col2:
        st.markdown("#### Mapa de correlación")
        corr = df.select_dtypes(include='number').corr()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig)

        st.markdown("#### Relación entre Asistencia y Nota Media")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.scatterplot(data=df, x="Asistencia",
                        y="Nota Media", hue="Abandono", ax=ax2)
        st.pyplot(fig2)

# Pie institucional
st.markdown("---")
st.caption("Demo académica construida con FastAPI, Streamlit y datos sintéticos. © 2025 Universidad Francisco de Vitoria.")
