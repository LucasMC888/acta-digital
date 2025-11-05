import streamlit as st
import hashlib, time, json
from pathlib import Path

# --- Función para generar el hash SHA-256 ---
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# --- Configuración de la aplicación ---
st.set_page_config(page_title="Registro de Documentos Digitales", page_icon="🧾")
st.title("🧾 Registro de Documentos Digitales")

st.write("""
Esta aplicación permite **registrar documentos digitales** mediante un hash único (SHA-256).  
Cada registro incluye el propietario, el contenido y la hora exacta del registro.  
El archivo resultante (`blockchain.json`) funciona como una **cadena de bloques simple**.
""")

# --- Entradas del usuario ---
owner = st.text_input("👤 Propietario del documento", placeholder="Ejemplo: Juan Pérez")
content = st.text_area("📝 Contenido del documento", placeholder="Escribe el texto completo del documento...")

# --- Acción: registrar documento ---
if st.button("🔐 Registrar documento"):
    if not owner.strip() or not content.strip():
        st.warning("Por favor, completa todos los campos antes de registrar.")
    else:
        record = {
            "owner": owner.strip(),
            "hash": get_hash(content),
            "time": time.time(),
            "readable_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Guardar el registro (una línea JSON por registro)
        with open("blockchain.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        st.success("✅ Documento registrado con éxito")
        st.code(record["hash"], language="bash")
        st.caption("Hash generado — guarda este valor para verificar la autenticidad del documento.")

# --- Mostrar los registros existentes ---
st.subheader("📜 Registros recientes")

blockchain_file = Path("blockchain.json")
if blockchain_file.exists():
    try:
        lines = blockchain_file.read_text(encoding="utf-8").strip().splitlines()
        if lines:
            last_records = [json.loads(l) for l in lines[-5:][::-1]]  # mostrar últimos 5
            for r in last_records:
                st.markdown(f"**{r['readable_time']} — {r['owner']}**")
                st.write("`", r['hash'][:20], "...`")
                with st.expander("Ver contenido"):
                    st.write(r["content"])
        else:
            st.info("No hay registros todavía.")
    except Exception as e:
        st.error(f"Error al leer registros: {e}")
else:
    st.info("No existe todavía el archivo `blockchain.json`.")

