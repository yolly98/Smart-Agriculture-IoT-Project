import getopt
import sys
import socket
import sys
import log
import json
import to_node
import from_node
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

nodes = dict()
my_ip = "fd00::1"
port = 5683

configs = dict()

def coapStatus(land_id, node_id, doc):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if  not (index in configs):
        configs[index] = dict()

    configs[index][doc['cmd']] = doc
    if (configs[index]['config-status'] 
        and configs[index]['irr-status'] 
        and configs[index]['mst-status']
        and configs[index]['ph-status']
        and configs[index]['light-status']
        and configs[index]['tmp-status']):

        irr_config = configs[index]['irr-status']
        mst_timer = configs[index]['mst-status']['timer']
        ph_timer = configs[index]['ph-status']['timer']
        light_timer = configs[index]['light-status']['timer']
        tmp_timer = configs[index]['tmp-status']['timer']

        msg = { 'cmd': 'status', 'body': { 'land_id': land_id, 'node_id': node_id, 'irr_config': { 'enabled': irr_config['enabled'], 'irr_limit': irr_config['irr_limit'], 'irr_duration': irr_config['irr_duration'] }, 'mst_timer': mst_timer, 'ph_timer': ph_timer, 'light_timer': light_timer, 'tmp_timer': tmp_timer } } 
        configs[index] = dict()
        from_node.status("COAP", msg)

# --------------- CLIENT---------------- #


def add_nodes(land_id, node_id, addr):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if (index in nodes) and nodes[index] == addr:
        return
    else:
        nodes[index] = addr
        client_observe(addr, "/irrigation")
        client_observe(addr, "/sensor/mst")
        client_observe(addr, "/sensor/ph")
        client_observe(addr, "/sensor/light")
        client_observe(addr, "/sensor/tmp")


def send_msg(land_id, node_id, path, mode, msg):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if not (index in nodes):
        log.log_err("Node address uknown")
        return
    
    host = nodes[index]
    client = HelperClient(server=(host, port))
    if mode == "GET":
        response = client.get(path)
    elif mode == "PUT":
        response = client.put(path, msg)
    
    log.log_info(f"received (coap) {response.payload}")

    doc = json.loads(response.payload)
    if doc['cmd'].find("status") >= 0:
        coapStatus(land_id, node_id, doc)
    elif doc['cmd'] == "irrigation":
        msg = { 'cmd': doc['cmd'], 'body': { 'land_id': land_id, 'node_id': node_id, 'status': doc['status'] } }
        from_node.irrigation(msg)
    elif doc['cmd'] == "mst":
        msg = { 'cmd':'moisture', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'moisture', 'value': doc['value'] } }
        from_node.moisture(msg)
    elif doc['cmd'] == "ph":
        msg = { 'cmd':'ph', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'ph', 'value': doc['value'] } }
        from_node.ph(msg)
    elif doc['cmd'] == "light":
        msg = { 'cmd':'light', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'light', 'value': doc['value'] } }
        from_node.light(msg)
    elif doc['cmd'] == "tmp":
        msg = { 'cmd':'tmp', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'tmp', 'value': doc['value'] } }
        from_node.tmp(msg)
    elif doc['cmd'] == "is_alive_ack":
        msg = { 'cmd': doc['cmd'], 'body': { 'land_id': land_id, 'node_id': node_id } }
        from_node.is_alive_ack(msg)
    #client.stop()

#def send_msg(addr, path):
#    
#    host = addr
#    client = HelperClient(server=(host, port))
#    response = client.get(path)
#    print(response.pretty_print())
#    #client.stop()

def client_callback(response):
    log.log_info(f"received from observing {response.payload}")
    addr = extract_addr(response)
    index = [ key for key in nodes.items() if key[1] == addr][0][0]
    index = index.replace("NODE/","")
    index = index.split("/")
    land_id = index[0]
    node_id = index[1]
    if response.payload == None:
        log.log_err("received Non from observing")
    doc = json.loads(response.payload)
    if doc['cmd'].find("status") >= 0:
        coapStatus(land_id, node_id, doc)
    elif doc['cmd'] == "irrigation":
        msg = { 'cmd': doc['cmd'], 'body': { 'land_id': land_id, 'node_id': node_id, 'status': doc['status'] } }
        from_node.irrigation(msg)
    elif doc['cmd'] == "mst":
        msg = { 'cmd':'moisture', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'moisture', 'value': doc['value'] } }
        from_node.moisture(msg)
    elif doc['cmd'] == "ph":
        msg = { 'cmd':'ph', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'ph', 'value': doc['value'] } }
        from_node.ph(msg)
    elif doc['cmd'] == "light":
        msg = { 'cmd':'light', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'light', 'value': doc['value'] } }
        from_node.light(msg)
    elif doc['cmd'] == "tmp":
        msg = { 'cmd':'tmp', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'tmp', 'value': doc['value'] } }
        from_node.tmp(msg)
    elif doc['cmd'] == "is_alive_ack":
        msg = { 'cmd': doc['cmd'], 'body': { 'land_id': land_id, 'node_id': node_id } }
        from_node.is_alive_ack(msg)

def client_observe(addr, path):
    
    host = addr
    client = HelperClient(server=(host, port))
    client.observe(path, client_callback)


# ------------ SERVER ---------------- #

def extract_addr(request):
    addr = str(request)
    addr = addr.split(",")
    addr = addr[0].split("(")
    addr = addr[1].split(",")
    addr = addr[0].replace("\'", "")
    return addr

class ConfigurationRes(Resource):

    def __init__(self, name="Config Portal", coap_server=None):
        super(ConfigurationRes, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "Basic Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        msg = json.loads(request.payload)
        addr = extract_addr(request)
        to_print = "received " + str(msg) + " from " + addr
        log.log_info(to_print)
        self.payload = to_node.assign_config(msg['land_id'], msg['node_id'], "COAP")
        add_nodes(msg['land_id'], msg['node_id'], addr)
        return self

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port), False)
        self.add_resource("new_config", ConfigurationRes())


def listener():

    server = CoAPServer(my_ip, port)

    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")