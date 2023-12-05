from machine import Pin 
from umqtt.simple import MQTTClient
import xtools,network
from machine import UART
import utime
com = UART(1, 9600, tx=17, rx=16)
com.init(9600)

def connect_wifi(ssid,password):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        print("Connecting to network...")
        sta.connect('kki', '0907308446')
        while not sta.isconnected():
            pass
    print("network config:", sta.ifconfig())
    
SSID = "kki"
PASSWORD = "0907308446"
connect_wifi(SSID,PASSWORD)

xtools.connect_wifi_led()
button = Pin(0,Pin.IN,Pin.PULL_UP)
topic_pub=b'topic/bell'
client_id = xtools.get_id()
mqtt_server = '172.20.10.13'

def connect_mqtt():
  global client_id, mqtt_server
  #client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client = MQTTClient (client_id,mqtt_server,keepalive=60)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  utime.sleep(10)
  machine.reset()


try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()
  
while True:
    try:
        while True:
            if button.value() == 0:
                utime.sleep_ms(10)  # 延遲時間是避免彈跳 不然訊息會炸開
            if button.value() == 0:
               message = "Warning! Someone ring the bell."
               print(message)
               client.publish(topic_pub,message)
            while not button.value():
                pass
    except OSError as e:
        restart_and_reconnect()
    
        
