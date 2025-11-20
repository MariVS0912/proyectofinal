# pages/2_Asistente.py
import streamlit as st
import sys, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from mqtt_logic import publish_message

st.title("Asistente — Control por texto")

st.write("Escribe comandos sencillos como: 'encender luz', 'apagar luz', 'abrir puerta', 'cerrar puerta', 'poner puerta 30'")

cmd = st.text_input("Escribe tu comando:")
if st.button("Enviar comando"):
    if not cmd:
        st.warning("Escribe algo primero")
    else:
        txt = cmd.lower()
        sent = False
        if "luz" in txt:
            if "encender" in txt or "prender" in txt:
                publish_message("casa/acciones/luz", "ON")
                st.success("Encendiendo luz")
                sent = True
            elif "apagar" in txt or "apagar" in txt:
                publish_message("casa/acciones/luz", "OFF")
                st.success("Apagando luz")
                sent = True
        if "puerta" in txt or "door" in txt:
            if "abrir" in txt or "open" in txt:
                publish_message("casa/acciones/puerta", "OPEN")
                st.success("Abriendo puerta")
                sent = True
            elif "cerrar" in txt or "close" in txt:
                publish_message("casa/acciones/puerta", "CLOSE")
                st.success("Cerrando puerta")
                sent = True
            else:
                # buscar número para ángulo
                import re
                m = re.search(r"(\d{1,3})", txt)
                if m:
                    angle = int(m.group(1))
                    angle = max(0, min(180, angle))
                    publish_message("casa/acciones/puerta", str(angle))
                    st.success(f"Moviendo puerta a {angle}°")
                    sent = True

        if not sent:
            st.info("No se detectó acción clara. Intenta: 'encender luz', 'abrir puerta', o 'puerta 45'.")
