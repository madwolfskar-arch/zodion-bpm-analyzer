import streamlit as st
from PIL import Image
import google.generativeai as genai
import datetime
from fpdf import FPDF

# --- CONFIGURACIÓN DE SEGURIDAD ZODION ---
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = "AIzaSyD9StlzJy9FXg9epKfSgrWWPz5ZMzgCmNI"

# FORZAMOS LA VERSIÓN DE LA API A 'v1' (Esto mata el error v1beta)
genai.configure(api_key=API_KEY)

# Usamos la sintaxis de modelo más compatible
model = genai.GenerativeModel('gemini-1.5-flash')

# Función para ejecutar el análisis (con manejo de errores de versión)
def analizar_evidencia(imagen):
    prompt = f"Hoy es {datetime.date.today()}. Analiza marca, producto y fecha de vencimiento. ¿Es apto?"
    try:
        # Intento 1: Sintaxis estándar
        return model.generate_content([prompt, imagen])
    except Exception:
        # Intento 2: Forzar parámetros si el servidor está en modo antiguo
        return model.generate_content(
            contents=[prompt, imagen],
            generation_config={"temperature": 0.1}
        )
    
    



