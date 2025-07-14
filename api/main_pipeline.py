from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

# 📍 Construir ruta absoluta al archivo del modelo
base_path = Path(__file__).resolve().parent.parent
model_path = base_path / "models" / "pipeline_nota_media.joblib"

# 🔄 Cargar el pipeline
pipeline = joblib.load(model_path)

app = FastAPI(title="Predicción de Nota Media", version="1.0")


class Estudiante(BaseModel):
    Edad: int
    Asignaturas: int
    Porcentaje_Exámenes_Aprobados: float
    Asistencia: float
    Uso_Biblioteca: int
    Estado_Emocional: int
    Curso: str
    Grado: str
    Facultad: str
    Sexo: str
    Nacionalidad: str
    Tipo_de_Acceso: str
    Beca: str
    Abandono: str


@app.post("/predecir")
def predecir_nota(data: Estudiante):
    datos = pd.DataFrame([data.dict()])

    # Renombrar columnas si es necesario
    datos.columns = [col.replace("_", " ") for col in datos.columns]

    prediccion = pipeline.predict(datos)[0]
    return {"Nota Media Estimada": round(prediccion, 2)}
