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

def client_observe(land_id, node_id, path):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if not index in nodes:
        return
    client = nodes[index]['host']
    client.observe(path, client_callback)

#----------------------

def add_nodes(land_id, node_id, addr):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if index not in nodes:
        nodes[index] = dict()
        nodes[index]['addr'] = addr
        nodes[index]['host'] = new_client(addr)
        return True
    elif (index in nodes) and nodes[index]['addr'] != addr:
        return False
    else:
        return True
        
def check_node(land_id, node_id):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if index in nodes:
        return True
    else:
        return False

def show_coap_nodes():

    log.log_console("+---------------------------------+")
    log.log_console("|       CONFIGURED COAP NODES     |")
    log.log_console("+---------------------------------+")
    for key in nodes.keys():
        log.log_console(f"  index: {key} | addr: {nodes[key]['addr']}")
    log.log_console("-----------------------------------")


def delete_node(land_id, node_id):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    log.log_info(f"deleting node ({land_id}, {node_id}) from cache")
    if index in nodes:
        nodes[index]['host'].stop()
        nodes.pop(index)

def get_nodes():
    list_of_nodes = []
    for key in nodes.keys():
        index = (key.replace("NODE/", "")).split('/')
        list_of_nodes.append({'land_id': index[0], 'node_id': index[1], 'protocol': 'COAP', 'addr': nodes[key]['addr']})
    return list_of_nodes

def get_node_addr(land_id, node_id):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if index in nodes:
        return nodes[index]['addr']
    else:
        return False
#----------------------

def coap_reset_config(land_id, node_id):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if index not in configs:
        return
    configs[index].pop('irr-status')
    configs[index].pop('mst-status')
    configs[index].pop('ph-status')
    configs[index].pop('light-status')
    configs[index].pop('tmp-status')

def coap_status(land_id, node_id, doc):
    index = "NODE/" + str(land_id) + "/" + str(node_id)
    if not (index in configs):
        configs[index] = dict()
        configs[index]['observed'] = False

    configs[index][doc['cmd']] = doc
    if ('config-status' in configs[index] and
        'irr-status' in configs[index] and
        'mst-status' in configs[index] and
        'ph-status' in configs[index] and
        'light-status' in configs[index] and
        'tmp-status'in configs[index] 
        ):

        if configs[index]['observed'] == False:
            log.log_info(f"Observing node ({land_id}, {node_id})")
            client_observe(land_id, node_id, "/irrigation")
            client_observe(land_id, node_id, "/sensor/mst")
            client_observe(land_id, node_id, "/sensor/ph")
            client_observe(land_id, node_id, "/sensor/light")
            client_observe(land_id, node_id, "/sensor/tmp")

        configs[index]['observed'] = True

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
    
    client = new_client(nodes[index]['addr'])
    response = None
    if mode == "GET":
        response = client.get(path, timeout=SEND_TIMEOUT)
    elif mode == "PUT":
        response = client.put(path, msg, timeout=SEND_TIMEOUT)
    
    client.stop()
    if response == None or response.payload == None or response.payload == "":
        return False
    return client_callback(response)

#----------------------

def client_callback(response):

    if response == None:
        log.log_err("received None")
        return False
    addr = extract_addr(response)
    index = [ key for key in nodes.items() if key[1]['addr'] == addr][0][0]
    index = index.replace("NODE/","")
    index = index.split("/")
    land_id = index[0]
    node_id = index[1]

    if response.payload == None or response.payload == "":
        log.log_err(f"received None from ({land_id}, {node_id})")
        return False

    if response.payload == "TooManyObservers":
        log.log_err(f"error too many oberservers in node ({land_id}, {node_id})")
        return False
    
    doc = json.loads(response.payload)
    log.log_receive(doc, land_id, node_id)

    if doc['cmd'].find("status") >= 0:
        if doc['cmd'] == 'config-status':
            if int(doc['body']['land_id']) != int(land_id) or int(doc['body']['node_id']) != int(node_id):
                log.log_err(f"node {land_id}, {node_id} address is changed")
                update_mysql_db.update_address_in_configuration(land_id, node_id, "null", "null")
                delete_node(land_id, node_id)
                return False

        coap_status(land_id, node_id, doc)
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
        from_node.is_alive_ack(msg, "COAP")

    return True

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
        log.log_receive(str(msg), addr, 0)
        if (not check_node(msg['land_id'], msg['node_id']) 
            or ( check_node(msg['land_id'], msg['node_id']) and (not add_nodes(msg['land_id'], msg['node_id'], addr) ))
            ):
            self.payload = to_node.assign_config(msg['land_id'], msg['node_id'], "COAP", addr, False)
        else:
            client_observe(msg['land_id'], msg['node_id'], "/irrigation")
            client_observe(msg['land_id'], msg['node_id'], "/sensor/mst")
            client_observe(msg['land_id'], msg['node_id'], "/sensor/ph")
            client_observe(msg['land_id'], msg['node_id'], "/sensor/light")
            client_observe(msg['land_id'], msg['node_id'], "/sensor/tmp")
            self.payload = "server-ok"
        return self

#----------------------

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