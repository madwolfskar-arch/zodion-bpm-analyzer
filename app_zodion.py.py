import streamlit as st
from PIL import Image
import google.generativeai as genai
import datetime
from fpdf import FPDF

# --- CONFIGURACIÓN ELITE ZODION (NUBE & SEGURIDAD) ---
# Intentamos obtener la clave de los Secrets de la nube; si no, usamos la de respaldo
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = "AIzaSyD9StlzJy9FXg9epKfSgrWWPz5ZMzgCmNI"

# Configuración forzada para evitar el error 404 de la versión beta
genai.configure(api_key=API_KEY)

# Cargamos el modelo usando la ruta absoluta más estable
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.set_page_config(page_title="ZODION - Panel de Inspección", layout="wide", page_icon="🛡️")

# --- LÓGICA DE REPORTES PDF ---
class ZodionReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'ZODION SERVICIOS AMBIENTALES - REPORTE TÉCNICO', 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, f'Pasto, Nariño | Fecha: {datetime.date.today()}', 0, 1, 'C')
        self.ln(10)

def generar_pdf_bytes(check_datos, hallazgo, accion, analitica):
    pdf = ZodionReport()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    pdf.set_fill_color(230, 240, 255)
    pdf.cell(0, 10, "ESTADO DE CUMPLIMIENTO (CHECKLIST)", 1, 1, 'L', True)
    for k, v in check_datos.items():
        pdf.cell(0, 8, f"{'OK' if v else 'NO CUMPLE'} - {k}", 0, 1)
    
    pdf.ln(5)
    pdf.set_fill_color(230, 240, 255)
    pdf.cell(0, 10, "ANÁLISIS DE TRAZABILIDAD IA (VISIÓN)", 1, 1, 'L', True)
    pdf.multi_cell(0, 8, analitica.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf.ln(5)
    pdf.set_fill_color(255, 230, 230)
    pdf.cell(0, 10, "SECCIÓN 12: ACCIONES CORRECTIVAS", 1, 1, 'L', True)
    pdf.multi_cell(0, 8, f"HALLAZGO: {hallazgo}\nACCIÓN: {accion}".encode('latin-1', 'replace').decode('latin-1'))
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- INTERFAZ DE USUARIO ---
st.title("🛡️ Sistema de Gestión Ambiental Zodion")
st.write(f"Soporte Técnico Especializado | Hoy es: {datetime.date.today()}")

checklist = {}
with st.sidebar:
    st.header("Checklist de Inspección")
    checklist["Integridad Estructural"] = st.checkbox("Equipos sin óxido/fisuras")
    checklist["Cierre de Puertas"] = st.checkbox("Gomas y Empaques OK")
    t = st.number_input("Temperatura registrada (°C)", value=2.0)
    checklist[f"Temperatura Controlada ({t}°C)"] = st.checkbox("Dentro de rango (0-4°C)")

col1, col2 = st.columns(2)

# Inicializamos el estado del análisis para que sea persistente
if 'analisis_resultado' not in st.session_state:
    st.session_state.analisis_resultado = "Esperando análisis técnico..."

with col1:
    foto = st.file_uploader("Subir evidencia (Etiqueta/Equipo)", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, caption="Evidencia cargada", width=400)

with col2:
    if foto:
        if st.button("🚀 EJECUTAR ESCÁNER TÉCNICO"):
            with st.spinner("Analizando bajo estándares Zodion..."):
                try:
                    img = Image.open(foto)
                    # Forzamos la detección con un prompt directo
                    prompt = f"Analiza esta imagen de inspección BPM. Identifica producto, marca y fecha de vencimiento. Hoy es {datetime.date.today()}. Determina si es apto según la fecha actual."
                    response = model.generate_content([prompt, img])
                    st.session_state.analisis_resultado = response.text
                except Exception as e:
                    st.error(f"Nota técnica Zodion: No se pudo conectar con el motor. Error: {e}")

    st.info(st.session_state.analisis_resultado)

st.divider()
h_txt = st.text_area("Hallazgo (Sección 12)")
a_txt = st.text_area("Acción Correctiva")

if st.button("📄 FINALIZAR Y GENERAR REPORTE PDF"):
    pdf_out = generar_pdf_bytes(checklist, h_txt, a_txt, st.session_state.analisis_resultado)
    st.download_button("⬇️ Descargar Reporte Zodion", pdf_out, f"Zodion_{datetime.date.today()}.pdf", "application/pdf")

