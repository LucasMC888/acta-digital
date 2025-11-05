import streamlit as st

st.title("Acta Digital")
st.write("¡Bienvenido a tu aplicación con Streamlit!")

import streamlit as st
import hashlib, time, json


import streamlit as st
import hashlib, time, json
from pathlib import Path

# --- Funciones auxiliares ---
def calcular_hash(texto: str) -> str:
    """Calcula SHA-256 del texto dado y devuelve el hex digest."""
    h = hashlib.sha256()
    h.update(texto.encode("utf-8"))
    return h.hexdigest()

def guardar_registro(registro: dict, fichero="records.json"):
    """
    Guarda (anexa) un registro JSON en un fichero local.
    Nota: en Streamlit Cloud los ficheros locales persisten mientras la app esté desplegada,
    pero no reemplazan el repositorio en GitHub.
    """
    p = Path(fichero)
    datos = []
    if p.exists():
        try:
            datos = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            datos = []
    datos.append(registro)
    p.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")

# --- Interfaz Streamlit mínima ---
st.title("Acta Digital — Demo de imports básicos")
texto = st.text_area("Escribe el contenido a hashear", value="Ejemplo de acta...")

if st.button("Calcular hash y registrar"):
    ts = int(time.time())
    h = calcular_hash(texto)
    registro = {
        "timestamp": ts,
        "readable_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)),
        "content": texto,
        "sha256": h
    }
    guardar_registro(registro)
    st.success("Hash calculado y registro guardado localmente.")
    st.write("SHA-256:", h)
    st.json(registro)

# Mostrar últimos registros (si existen)
p = Path("records.json")
if p.exists():
    try:
        registros = json.loads(p.read_text(encoding="utf-8"))
        st.write("Registros almacenados (últimos 5):")
        for r in registros[-5:][::-1]:
            st.write(r["readable_time"], "-", r["sha256"][:12], "...")
    except Exception:
        st.warning("No se pudieron leer los registros.")






import streamlit as st
import hashlib, time, json

# --- Función para generar hash ---
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

st.title("🧾 Acta Digital — Generador de Hash Original")

st.write("Genera un hash único para tu acta o documento.")

# Campo de texto
texto = st.text_area("✍️ Escribe el texto del acta:", placeholder="Ejemplo: Reunión del comité...")

# Botón para generar hash
if st.button("🔐 Generar hash"):
    if texto.strip():
        hash_resultado = get_hash(texto)
        st.success("✅ Hash original generado correctamente.")
        st.write("**SHA-256:**")
        st.code(hash_resultado)
        st.info("Guarda este hash — es la huella digital del texto original.")
    else:
        st.warning("Por favor, escribe un texto antes de generar el hash.")






