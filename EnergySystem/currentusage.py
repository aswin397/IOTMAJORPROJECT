import paho.mqtt.client as paho
def on_msg(client, userdata, message):
    print ("Service") 
    global Str
    Str=str(message.payload.decode("utf-8"))
    if Str!="":
        print("Value is fetched")
        client1.disconnect()

client1 = paho.Client() #create new instance
def Usage():
    client1.on_message=on_msg #attach function to callback
    print("connecting to send brokerr")
    client1.connect("broker.hivemq.com", 1883, 60)
    client1.subscribe("voltage", qos=1)
    client1.loop_forever() 
    print(Str)
    return Str

