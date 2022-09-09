import getopt
import sys
import socket
import sys
import log
import json
import to_node
import from_node
from persistence import update_mysql_db
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

nodes = dict()
my_ip = "fd00::1"
port = 5683
SEND_TIMEOUT = 3.0
configs = dict()

#----------------------

def extract_addr(request):
    addr = str(request)
#    addr = addr.split(",")
#    addr = addr[0].split("(")
#    addr = addr[1].split(",")
#    addr = addr[0].replace("\'", "")
    addr = addr.split("(")
    addr = addr[1].split(")")
    addr = addr[0].split(',')
    addr = addr[0].replace("\'","")
    return addr

#----------------------

def new_client(addr):
    host = addr
    client = HelperClient(server=(host, port))
    return client

#----------------------

def client_observe(client, path):
    client.observe(path, client_callback)

#----------------------

def add_nodes(land_id, node_id, addr):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if (index in nodes) and nodes[index]['addr'] == addr:
        return
    else:
        nodes[index] = dict()
        nodes[index]['addr'] = addr
        nodes[index]['host'] = new_client(addr)

#----------------------

def show_coap_nodes():

    log.log_info("List of known nodes")
    keys = [ key for key, val in nodes.items()]
    for key in keys:
        print(f"index: {key} addr: {nodes[key]['addr']}")
    print("-----------------------")
        
#----------------------

def delete_node(land_id, node_id):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    log.log_info(f"deleting node {index} from cache")
    if index in nodes:
        nodes[index]['host'].stop()
        nodes.pop(index)

#----------------------

def coapStatus(land_id, node_id, doc):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if not (index in configs):
        configs[index] = dict()

    configs[index][doc['cmd']] = doc
    if ('config-status' in configs[index] and
        'irr-status' in configs[index] and
        'mst-status' in configs[index] and
        'ph-status' in configs[index] and
        'light-status' in configs[index] and
        'tmp-status'in configs[index] 
        ):

        irr_config = configs[index]['irr-status']['body']
        mst_timer = configs[index]['mst-status']['timer']
        ph_timer = configs[index]['ph-status']['timer']
        light_timer = configs[index]['light-status']['timer']
        tmp_timer = configs[index]['tmp-status']['timer']

        msg = { 'cmd': 'status', 'body': { 'land_id': land_id, 'node_id': node_id, 'irr_config': { 'enabled': irr_config['enabled'], 'irr_limit': irr_config['irr_limit'], 'irr_duration': irr_config['irr_duration'] }, 'mst_timer': mst_timer, 'ph_timer': ph_timer, 'light_timer': light_timer, 'tmp_timer': tmp_timer } } 
        from_node.status("COAP", nodes[index]['addr'], msg)

# --------------- CLIENT---------------- #

def send_msg(land_id, node_id, path, mode, msg):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if not (index in nodes):
        log.log_err(f"{index} address unknown")
        return False
    
    client = nodes[index]['host']
    if mode == "GET":
        response = client.get(path, timeout=SEND_TIMEOUT)
    elif mode == "PUT":
        response = client.put(path, msg, timeout=SEND_TIMEOUT)
    
    if response == None or response.payload == "" or response.payload == None:
        log.log_err(f"node {index} doesn't respond")
        return False

    log.log_info(f"received (coap) {response.payload}")

    doc = json.loads(response.payload)
    if doc['cmd'].find("status") >= 0:
        if doc['cmd'] == 'config-status':
            if doc['body']['land_id'] != int(land_id) or doc['body']['node_id'] != int(node_id):
                log.log_err(f"node {index} address is changed")
                update_mysql_db.update_address_in_configuration(land_id, node_id, "null", "null")
                delete_node(land_id, node_id)
                return
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
        log.log_success(f"node {index} online")
        msg = { 'cmd': doc['cmd'], 'body': { 'land_id': land_id, 'node_id': node_id } }
        from_node.is_alive_ack(msg)

    return True

#----------------------

def client_callback(response):

    if response == None:
        return
    addr = extract_addr(response)
    index = [ key for key in nodes.items() if key[1]['addr'] == addr][0][0]
    index = index.replace("NODE/","")
    index = index.split("/")
    land_id = index[0]
    node_id = index[1]

    log.log_info(f"received from observing {response.payload}")
    if response.payload == None:
        log.log_err("received None from observing")
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



# ------------ SERVER ---------------- #



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
        self.payload = to_node.assign_config(msg['land_id'], msg['node_id'], "COAP", addr)
        add_nodes(msg['land_id'], msg['node_id'], addr)
        index = f"NODE/{msg['land_id']}/{msg['node_id']}"
        client_observe(nodes[index]['host'], "/irrigation")
        client_observe(nodes[index]['host'], "/sensor/mst")
        client_observe(nodes[index]['host'], "/sensor/ph")
        client_observe(nodes[index]['host'], "/sensor/light")
        client_observe(nodes[index]['host'], "/sensor/tmp")
        return self

#----------------------

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port), False)
        self.add_resource("new_config", ConfigurationRes())

#----------------------

def listener():

    server = CoAPServer(my_ip, port)

    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")