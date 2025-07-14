import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurar la página
st.set_page_config(
    page_title="Datatools Demo",
    page_icon="📘",
    layout="centered"
)

# Estilo visual personalizado
st.markdown("""
<style>
    /* Fondo azul corporativo sólido */
    [data-testid="stAppViewContainer"] {
        background-color: #005ca9;
        background-image: none;
    }

    /* Títulos y botones */
    h1, h2, h3, label, .stButton>button {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px #000000;
    }

    /* Markdown sobre fondo oscuro semitransparente */
    .stMarkdown {
        background-color: rgba(0,0,0,0.6);
        padding: 1rem;
        border-radius: 0.5rem;
    }

    /* Contenedor del formulario */
    .stForm {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 1rem;
        backdrop-filter: blur(2px);
    }

    /* Inputs en blanco visible */
    .stSelectbox, .stNumberInput input {
        background-color: rgba(255,255,255,0.1) !important;
        color: #ffffff !important;
        border: none;
    }

    /* Sliders en azul corporativo UFV */
    [data-testid="stSlider"] > div {
        background: none !important;
    }

    [data-testid="stSlider"] .st-cq {
        background: linear-gradient(to right, #005ca9, #005ca9) !important;
    }

    [data-testid="stSlider"] .st-cr {
        color: #ffffff !important;
    }

    /* Botón en azul UFV */
    .stButton>button {
        background-color: #005ca9 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 0.3rem;
        padding: 0.5rem 1rem;
        border: none;
    }

    /* Ocultar pie de página de Streamlit */
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Logo institucional
st.image("assets/Logo_UFV.jpg", width=650)

# Pestañas
tab1, tab2 = st.tabs(["Predicción", "Visualización de Datos"])

with tab1:
    st.title("Datatools – Predicción de Nota Media")
    st.markdown("""
    Esta demo utiliza aprendizaje automático para estimar la nota media de un estudiante  
    según sus hábitos académicos, emocionales y comportamiento.
    """)

    with st.form("formulario_prediccion"):
        st.subheader("Datos del estudiante")

        edad = st.slider("Edad", min_value=17, max_value=40, value=0)
        asignaturas = st.number_input(
            "Asignaturas matriculadas", min_value=1, max_value=15, value=1)
        porcentaje = st.slider(
            "Porcentaje de Exámenes Aprobados", min_value=0.0, max_value=1.0, value=0.0)
        asistencia = st.slider(
            "Asistencia", min_value=0.0, max_value=1.0, value=0.0)
        biblioteca = st.selectbox(
            "Visitas a Biblioteca por mes", list(range(0, 16)), index=0)
        emocional = st.slider(
            "Estado Emocional (1 = Inestable, 5 = Estable)", min_value=1, max_value=5, value=1)
        enviado = st.form_submit_button("Estimar Nota Media")

    if enviado:
        url = "http://localhost:8000/predecir"
        datos = {
            "Edad": edad,
            "Asignaturas": asignaturas,
            "Porcentaje_Exámenes_Aprobados": porcentaje,
            "Asistencia": asistencia,
            "Uso_Biblioteca": biblioteca,
            "Estado_Emocional": emocional
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

    df = pd.read_csv("data/dataset_estudiantes.csv")

    st.markdown("#### Mapa de correlación")
    corr = df.select_dtypes(include='number').corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, fmt=".2f", annot=True, cmap="Blues", ax=ax)
    # Inclinamos etiquetas del eje X
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

    st.markdown("#### Relación entre Asistencia y Nota Media")
    df["Nota Media"] = (df["Nota Primer Semestre"] +
                        df["Nota Segundo Semestre"]) / 2
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=df, x="Asistencia",
                    y="Nota Media", hue="Abandono", ax=ax2)
    st.pyplot(fig2)

# Pie institucional
st.markdown("---")
st.caption("Demo académica construida con FastAPI, Streamlit y ciencia de datos. Esta interfaz es solo un ejemplo de presentación.")
