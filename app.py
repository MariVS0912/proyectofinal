import streamlit as st
# Importamos la función de conexión del archivo mqtt_logic.py que debe estar al lado
from mqtt_logic import iniciar_mqtt

# Configuración de la pestaña del navegador
st.set_page_config(page_title="Smart Home UOC", page_icon="🏠")

st.title("🏠 Smart Home: Proyecto Final")

# --- INICIALIZACIÓN DE VARIABLES ---
# Creamos el espacio en memoria para guardar los datos de los sensores
# Esto evita errores si la conexión tarda un poco
if "datos_sensores" not in st.session_state:
    st.session_state["datos_sensores"] = {
        "temp": 0, 
        "hum": 0, 
        "gas": 0, 
        "luz": 0
    }

# --- INICIO DE CONEXIÓN ---
# Esto arranca el motor MQTT apenas abres la app.
# Es crucial que mqtt_logic.py esté en la misma carpeta para que esto funcione.
iniciar_mqtt()

st.markdown("""
### Bienvenido al Sistema Multimodal

Esta aplicación cumple con los requisitos del proyecto final permitiendo controlar tu casa inteligente (simulada en Wokwi) de dos maneras distintas:

1.  **📊 Dashboard Visual:** Para control rápido mediante botones y lectura de métricas.
2.  **🗣️ Asistente Virtual:** Para control mediante lenguaje natural (Chat).

👈 **Usa el menú de la izquierda para navegar entre las interfaces.**
""")

# Indicador de estado para saber si Wokwi está conectado
if st.session_state.get("mqtt_connected"):
    st.success("✅ Sistema Conectado con Wokwi")
else:
    st.warning("⏳ Conectando al servidor MQTT...")

st.info("Recuerda tener la simulación de Wokwi corriendo para ver los cambios.")
