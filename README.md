## Predicción de Nota Media – API con FastAPI

Proyecto de Machine Learning para predecir la **nota media** de estudiantes universitarios. Utiliza un modelo entrenado con `scikit-learn` y está desplegado mediante una API REST construida con **FastAPI**.

---

## Estructura del proyecto

prediccion_nota_media/ ├── entorno/ # Entorno virtual local ├── main.py # API REST (FastAPI) ├── notebook.ipynb # Notebook con exploración y entrenamiento ├── modelo_nota_media.joblib # Modelo guardado ├── features_modelo.joblib # Variables usadas por el modelo ├── requirements.txt # Dependencias exactas del proyecto ├── README.md # Documentación del proyecto

![[estructura.png]]
---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/prediccion_nota_media.git
cd prediccion_nota_media
```
```

```


### 2. Crear entorno virtual dentro del proyecto

```bash
python -m venv entorno_ufv_fastapi
```
### 3. Activar el entorno
Windows:

```
entorno_ufv_fastapi\Scripts\activate
```


### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### Lanzar la API
```bash
uvicorn main:app --reload

o 

python -m uvicorn main:app --reload
```
Accede a la documentación interactiva: http://localhost:8000/docs

###  Uso del endpoint /predecir

```bash
POST /predecir
```

### Ejemplo de entrada:

```bash

json
{
  "Edad": 20,
  "Asignaturas": 5,
  "Porcentaje_Exámenes_Aprobados": 85.0,
  "Asistencia": 92.0,
  "Uso_Biblioteca": 3,
  "Estado_Emocional": 2
}
```

### Respuesta esperada:
```bash

json
{
  "Nota Media Estimada": 7.64
}
```
### Con streamlit, lanzar streamlit
```bash
streamlit run interfaz_dobletab.py

o

python -m streamlit run interfaz_dobletab.py
o 
python -m streamlit run interfaz_pipeline.py
```
### Requisitos técnicos
- Python 3.10+

- FastAPI

- scikit-learn

- pandas, numpy, seaborn, matplotlib

- joblib

- uvicorn

- Streamlit

Autor
José Telle