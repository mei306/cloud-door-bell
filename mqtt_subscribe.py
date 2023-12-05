import paho.mqtt.client as mqtt
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import TextSendMessage

linebot_api = LineBotApi("cejon4trTMixjusA6HUl99T1rXnAM6F8zdnDBylOtlkIaXIwLoIwud+9RMSkiY7nI1hNbC3gShLjnlF9lrxF6yq+RRKmy4Dz2/0SC3V1MLv4Fd11DGbybjWeagQn7qjn0Hmg1rCP2IudF7G3aftwOgdB04t89/1O/w1cDnyilFU=") #channel acess token
handler = WebhookHandler("d052f047459d090e8e025b7c001f80f4")#channel secret

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("topic/bell")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #mqtt message send to linebot
    message = TextSendMessage(text=msg.payload.decode("utf-8"))
    linebot_api.broadcast(message)
    
   

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.20.10.4", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_forever()