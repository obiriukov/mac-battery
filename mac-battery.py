import subprocess
import json
import datetime
import platform
import paho.mqtt.client as mqtt
import socket
import os
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()

def get_battery_status():
    result = subprocess.run(
        ["pmset", "-g", "batt"],
        stdout=subprocess.PIPE,
        text=True
    )
    for line in result.stdout.splitlines():
        if ";" in line:
            parts = line.split(";")
            if len(parts) > 1:
                status = parts[1].strip()
            return status
    return None

# Отримати інформацію про батарею
def get_battery_percent():
    result = subprocess.run(
        ["pmset", "-g", "batt"],
        stdout=subprocess.PIPE,
        text=True
    )
    for line in result.stdout.splitlines():
        if "%" in line:
            percent = int(line.split('\t')[-1].split('%')[0].strip())
            return percent
    return None

MQTT_USERNAME = os.getenv("MQTT_USERNAME", "mqtt-user")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "mqtt-password")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", platform.node())

print(f"MQTT Configuration: {MQTT_USERNAME}, {MQTT_PASSWORD}, {MQTT_HOST}, {MQTT_PORT}, {MQTT_TOPIC}")

def publish_to_mqtt(topic, payload):
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    result = client.publish(topic, payload)
    result.wait_for_publish()
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Message sent successfully to topic:" + topic + " with payload: " + str(payload))
    else:
        print(f"Failed to send message, error code: {result.rc}")
    client.disconnect()

def publish_battery_level(level):
    publish_to_mqtt(f"{MQTT_TOPIC}/battery/level", level)

def publish_battery_status(status):
    publish_to_mqtt(f"{MQTT_TOPIC}/battery/status", status)

def publish_update_time():
    publish_to_mqtt(f"{MQTT_TOPIC}/battery/update_time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    battery_level = get_battery_percent()
    battery_status = get_battery_status()
    if battery_level is not None:
        publish_battery_level(battery_level)
    if battery_status is not None:
        publish_battery_status(battery_status)
    publish_update_time()