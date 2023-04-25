import paho.mqtt.client as mqtt
import environment

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

def mqttSetup():
    environment.mqttClient = mqtt.Client(client_id="home-automation-Pi")
    environment.mqttClient.on_connect = on_connect
    environment.mqttClient.on_disconnect = on_disconnect
    environment.mqttClient.connect("192.168.0.191", 1883, 60)
    environment.mqttClient.loop_forever()

