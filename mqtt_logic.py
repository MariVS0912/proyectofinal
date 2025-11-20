# mqtt_logic.py
import paho.mqtt.client as mqtt
import streamlit as st
import threading
import time

# Broker por defecto (pruebas)
DEFAULT_BROKER = "broker.hivemq.com"
DEFAULT_PORT = 1883

# topics
SENSORS_TOPIC_BASE = "casa/sensores/"
ACTIONS_TOPIC_BASE = "casa/acciones/"

# ---------------- MQTT callbacks ----------------
def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("🔌 Conectado al broker MQTT")
        # suscribir a sensores para mostrar en la app
        client.subscribe(SENSORS_TOPIC_BASE + "#")
        # suscribir también a topic de estado de dispositivos (opcional)
        client.subscribe("casa/sensores/#")
    else:
        print("❌ Error al conectar, rc=", rc)

def _on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print("MQTT ←", topic, payload)

    # Mantener en session_state
    st.session_state.setdefault("sensores", {})
    st.session_state.setdefault("dispositivos", {})

    if topic.startswith(SENSORS_TOPIC_BASE):
        key = topic.replace(SENSORS_TOPIC_BASE, "")
        st.session_state["sensores"][key] = payload
    else:
        # otros topics de estado o eco
        st.session_state["dispositivos"][topic] = payload

# ---------------- Conexión y cliente global ----------------
def connect_mqtt(broker=DEFAULT_BROKER, port=DEFAULT_PORT, client_id="streamlit_mqtt_client", username=None, password=None):
    """
    Conecta el cliente MQTT y guarda en st.session_state['mqtt_client'].
    Si ya existe, devuelve el existente.
    """
    if "mqtt_client" in st.session_state:
        return st.session_state["mqtt_client"]

    client = mqtt.Client(client_id=client_id, clean_session=True)
    if username and password:
        client.username_pw_set(username, password)
    client.on_connect = _on_connect
    client.on_message = _on_message

    try:
        client.connect(broker, port, keepalive=60)
        client.loop_start()
        st.session_state["mqtt_client"] = client
        st.session_state.setdefault("sensores", {})
        st.session_state.setdefault("dispositivos", {})
        st.session_state["mqtt_info"] = {"broker": broker, "port": port}
        return client
    except Exception as e:
        st.error(f"⚠ No se pudo conectar al broker: {e}")
        print("Error connect mqtt:", e)
        return None

def publish_message(topic, payload):
    client = st.session_state.get("mqtt_client")
    if not client:
        st.warning("No hay cliente MQTT conectado. Presiona 'Conectar MQTT' en la barra lateral.")
        return False
    client.publish(topic, payload)
    # Guardar estado local para feedback inmediato
    st.session_state.setdefault("dispositivos", {})
    st.session_state["dispositivos"][topic] = payload
    return True

def get_sensor_data(sensor_key):
    return st.session_state.get("sensores", {}).get(sensor_key, "N/A")

def get_device_status(topic):
    return st.session_state.get("dispositivos", {}).get(topic, "OFF")

