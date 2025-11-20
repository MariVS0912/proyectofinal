# pages/1_Dashboard.py
import streamlit as st
import sys, os

# asegurarnos de que la raíz esté en sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from mqtt_logic import publish_message, get_device_status, get_sensor_data

st.title("Dashboard — Controles")

st.header("Actuadores")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Luz")
    estado_luz = get_device_status("casa/acciones/luz")
    st.write("Estado local:", estado_luz)
    if st.button("Encender Luz"):
        publish_message("casa/acciones/luz", "ON")
        st.success("Mensaje ON enviado")
    if st.button("Apagar Luz"):
        publish_message("casa/acciones/luz", "OFF")
        st.info("Mensaje OFF enviado")

with col2:
    st.subheader("Puerta (Servo)")
    angulo = st.slider("Ángulo puerta", 0, 180, 90)
    if st.button("Mover puerta"):
        publish_message("casa/acciones/puerta", str(angulo))
        st.success(f"Pedido mover a {angulo}° enviado")
    if st.button("Abrir puerta (OPEN)"):
        publish_message("casa/acciones/puerta", "OPEN")
    if st.button("Cerrar puerta (CLOSE)"):
        publish_message("casa/acciones/puerta", "CLOSE")

st.markdown("---")
st.header("Sensores (últimos valores)")
sens = st.session_state.get("sensores", {})
if sens:
    for k, v in sens.items():
        st.metric(label=k, value=v)
else:
    st.info("No hay lecturas de sensores aún. Espera 2s para que el ESP32 publique.")
