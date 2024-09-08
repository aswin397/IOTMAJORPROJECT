import paho.mqtt.client as mqtt
import uuid

client_id = str(uuid.uuid4())

import paho.mqtt.client as mqtt

def on_msg(client, userdata, message):
    print("Service")
    global Str
    Str = str(message.payload.decode("utf-8"))
    if Str != "1":
        print("Value is fetched")
        client.disconnect()

client1 = mqtt.Client(client_id=client_id)


def previousmonth():
    global Str
    Str = ""
    client1.on_message = on_msg
    print("Connecting to broker")
    client1.connect("broker.hivemq.com", 1883, 60)
    client1.subscribe("lastmonth", qos=1)
    client1.loop_forever()
    print(Str)
    return Str


