# Imagen base oficial de Python
FROM python:3.11-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias
COPY requirements.txt ./

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código al contenedor
COPY . .

# Exponemos puertos de FastAPI y Streamlit
EXPOSE 8000
EXPOSE 8501

# Comando para ejecutar ambos servicios (puedes ajustar esto según tu estructura)
CMD ["sh", "-c", "uvicorn api.main_pipeline:app --host 0.0.0.0 --port 8000 & streamlit run interfaz_pipeline.py --server.port 8501"]
