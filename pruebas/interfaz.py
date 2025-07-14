import streamlit as st
import requests

# 🧭 Configurar la página
st.set_page_config(
    page_title="Datatools Demo",
    page_icon="📘",
    layout="centered"
)

# 🖼️ Estilo visual personalizado
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("assets/2702232.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
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
    .stSelectbox, .stSlider, .stNumberInput {
        color: white !important;
    }
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# 🎓 Logo institucional
st.image("assets/Logo_UFV.jpg", width=150)

# 📘 Título y descripción
st.title("📊 Datatools – Predicción de Nota Media")
st.markdown("""
Esta demo utiliza aprendizaje automático para estimar la nota media de un estudiante  
según sus hábitos académicos, emocionales y comportamiento 📚📈
""")

# 📝 Formulario de entrada
with st.form("formulario_prediccion"):
    st.subheader("📥 Datos del estudiante")

    edad = st.slider("Edad", 17, 40, 22)
    asignaturas = st.number_input(
        "Asignaturas matriculadas", min_value=4, max_value=15, value=7)
    porcentaje = st.slider("Porcentaje de Exámenes Aprobados", 0.0, 1.0, 0.85)
    asistencia = st.slider("Asistencia", 0.6, 1.0, 0.9)
    biblioteca = st.selectbox(
        "Visitas a Biblioteca por mes", list(range(0, 16)))
    emocional = st.slider(
        "Estado Emocional (1 = Inestable, 5 = Estable)", 1, 5, 3)

    enviado = st.form_submit_button("🔎 Estimar Nota Media")

# 🔍 Conexión con API
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
            st.success(f"🎯 Nota Media Estimada: {nota}")
        else:
            st.error("❌ Error al conectar con la API.")
    except Exception as e:
        st.error(f"⚠️ Conexión fallida: {e}")

# 📎 Pie institucional
st.markdown("---")
st.caption("🔬 Demo académica construida con FastAPI, Streamlit y ciencia de datos. Esta interfaz es solo un ejemplo visual de presentación.")
