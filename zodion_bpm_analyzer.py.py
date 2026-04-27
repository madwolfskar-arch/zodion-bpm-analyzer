import sys
import os
# Forzamos a Python a mirar en la carpeta donde el instalador dice que están las cosas
sys.path.append(r'C:\Users\Usuario Principal\AppData\Roaming\Python\Python314\site-packages')

import streamlit as st
from PIL import Image
from google import genai 
import datetime
from fpdf2 import FPDF 

# ... (resto del código igual)

# --- SIGUE EL RESTO DEL CÓDIGO IGUAL ---

# --- 1. CONFIGURACIÓN DE SEGURIDAD ZODION ---
# Puente de seguridad para evitar el error "SecretNotFoundError" en PC local
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        API_KEY = "AIzaSyD9StlzJy9FXg9epKfSgrWWPz5ZMzgCmNI"
except Exception:
    # Si falla la lectura de secretos (entorno local), usa la llave directa
    API_KEY = "AIzaSyD9StlzJy9FXg9epKfSgrWWPz5ZMzgCmNI"

# Inicialización del cliente con tecnología GenAI 2026
client = genai.Client(api_key=API_KEY)

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="ZODION - BPM Analyzer", 
    layout="wide", 
    page_icon="🛡️"
)

# Estilo visual de élite
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #003366; color: white; }
    </style>
    """, unsafe_allow_stdio=True)

# --- 3. LÓGICA DE REPORTES PDF ---
class ZodionReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'ZODION SERVICIOS AMBIENTALES - REPORTE BPM', 0, 1, 'C')
        self.ln(10)

# --- 4. INTERFAZ DE USUARIO ---
st.title("🛡️ Sistema de Gestión Ambiental Zodion")
st.subheader("Analizador de Evidencia y Estándares BPM")
st.write(f"Fecha de Auditoría: **{datetime.date.today()}**")

if 'analisis' not in st.session_state:
    st.session_state.analisis = "Esperando carga de evidencia técnica..."

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📸 Evidencia Fotográfica")
    foto = st.file_uploader("Cargar imagen (Etiquetas, Lotes, Productos)", type=["jpg", "png", "jpeg"])
    
    if foto:
        img_display = Image.open(foto)
        st.image(img_display, caption="Evidencia para análisis", use_container_width=True)

with col2:
    st.markdown("### 🔍 Resultados del Escáner")
    
    if foto and st.button("🚀 EJECUTAR ANÁLISIS TÉCNICO"):
        with st.spinner("Procesando con Inteligencia Artificial GenAI..."):
            try:
                img_logic = Image.open(foto)
                # Consulta avanzada para estándares de sanidad
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[
                        "Actúa como experto en BPM (Buenas Prácticas de Manufactura). "
                        "Analiza esta imagen detalladamente: identifica marca, lote y fecha de vencimiento. "
                        "Determina si cumple con estándares de sanidad ambiental y emite un veredicto técnico.", 
                        img_logic
                    ]
                )
                st.session_state.analisis = response.text
            except Exception as e:
                st.error(f"Error técnico Zodion: {e}")

    # Cuadro de resultados
    st.info(st.session_state.analisis)

    # Generación de PDF
    if st.session_state.analisis != "Esperando carga de evidencia técnica...":
        if st.button("📄 GENERAR REPORTE FORMAL"):
            try:
                pdf = ZodionReport()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Fecha: {datetime.date.today()}")
                pdf.ln(5)
                pdf.multi_cell(0, 10, f"RESULTADO DEL ANÁLISIS:\n\n{st.session_state.analisis}")
                
                pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
                st.download_button(
                    label="⬇️ Descargar Reporte en PDF",
                    data=pdf_output,
                    file_name=f"Reporte_BPM_Zodion_{datetime.date.today()}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error al generar PDF: {e}")













