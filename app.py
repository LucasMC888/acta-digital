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
from pathlib import Path

# --- Función para calcular el hash ---
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# --- Función para guardar los registros en un archivo JSON ---
def save_record(content, hash_value):
    record = {
        "timestamp": int(time.time()),
        "readable_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "content": content,
        "sha256": hash_value
    }

    # Cargar registros existentes (si el archivo ya existe)
    path = Path("records.json")
    records = []
    if path.exists():
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            records = []

    # Añadir el nuevo registro
    records.append(record)
    path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

# --- Interfaz de usuario Streamlit ---
st.title("🧾 Acta Digital — Sistema de Hash Seguro")

st.write("Esta aplicación genera un hash único (SHA-256) para registrar el contenido de un acta o texto.")

texto = st.text_area("✍️ Escribe el texto del acta:", placeholder="Ejemplo: Reunión del comité...")

if st.button("🔐 Generar hash y guardar registro"):
    if texto.strip():
        hash_resultado = get_hash(texto)
        save_record(texto, hash_resultado)
        st.success("✅ Hash generado y registro guardado correctamente.")
        st.write("**SHA-256:**", hash_resultado)
    else:
        st.warning("Por favor, escribe algún texto antes de generar el hash.")

# --- Mostrar registros guardados ---
st.subheader("📜 Últimos registros")
path = Path("records.json")
if path.exists():
    try:
        registros = json.loads(path.read_text(encoding="utf-8"))
        if registros:
            for r in registros[-5:][::-1]:
                st.markdown(f"**{r['readable_time']}** — `{r['sha256'][:16]}...`")
                with st.expander("Ver contenido"):
                    st.write(r["content"])
        else:
            st.info("No hay registros todavía.")
    except Exception:
        st.error("Error al leer los registros.")
else:
    st.info("Aún no hay registros guardados.")

