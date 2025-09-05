
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Cargar modelo y columnas
modelo = joblib.load('modelo_nota_media.joblib')
features = joblib.load('features_modelo.joblib')

app = FastAPI(title="Predicción de Nota Media", description="API REST para estudiantes", version="1.0")

class Estudiante(BaseModel):
    Edad: int
    Asignaturas: int
    Porcentaje_Exámenes_Aprobados: float
    Asistencia: float
    Uso_Biblioteca: int
    Estado_Emocional: int

@app.post("/predecir")
def predecir_nota(data: Estudiante):
    datos = pd.DataFrame([data.dict()])
    for col in features:
        if col not in datos.columns:
            datos[col] = 0
    datos = datos[features]
    prediccion = modelo.predict(datos)[0]
    return {"Nota Media Estimada": round(prediccion, 2)}
