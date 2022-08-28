import paho.mqtt.client as mqtt
import json
import from_node
# The callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("SERVER")

def parse_json(payload):
    json_doc = json.loads(payload[1:len(payload)-1])
    return json_doc

# The callback for when a PUBLISH message is received from the broker.
def on_message(client, userdata, msg):
    payload = (str(msg.payload))[1:]
    doc = parse_json(payload)
    if doc['cmd'] == 'config_rqst':
        from_node.config_request("MQTT", doc)
    elif doc['cmd'] == 'status':
        from_node.status("MQTT", doc)
    elif doc['cmd'] == 'irrigation':
        from_node.irrigation(doc)
    elif doc['cmd'] == 'moisture':
        from_node.moisture(doc)
    elif doc['cmd'] == 'ph':
        from_node.ph(doc)
    elif doc['cmd'] == 'light':
        from_node.light(doc)
    elif doc['cmd'] == 'tmp':
        from_node.tmp(doc)
    elif doc['cmd'] == 'is_alive_ack':
        from_node.is_alive_ack(doc)

client = mqtt.Client()

def mqtt_init():
    global client 
    client.connect("127.0.0.1", 1883, 60)

def mqtt_subscribe():
    global client
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

def mqtt_publish(topic, msg):
    global client
    client.publish(topic, payload=msg)