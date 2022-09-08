import getopt
import sys
import socket
import sys
import log
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

nodes = dict()
my_ip = "0.0.0.0"
port = 5683

# --------------- CLIENT---------------- #


def add_nodes(land_id, node_id, addr):
    index = "NODE/" + land_id + "/" + node_id
    if nodes[index] and nodes[index] == addr:
        return
    else:
        nodes[index] = addr
        client_observe(addr, "/irrigation")
        client_observe(addr, "/sensor/mst")
        client_observe(addr, "/sensor/ph")
        client_observe(addr, "/sensor/light")
        client_observe(addr, "/sensor/tmp")


def send_msg(land_id, node_id, path):
    index = "NODE/" + land_id + "/" + node_id
    if not nodes[index]:
        log.log_err("Node address uknown")
        return
    
    host = nodes[index]
    client = HelperClient(server=(host, port))
    response = client.get(path)
    print(response.pretty_print())
    #client.stop()

def send_msg(addr, path):
    
    host = addr
    client = HelperClient(server=(host, port))
    response = client.get(path)
    print(response.pretty_print())
     #client.stop()

def client_callback(response):
    log.log_receive(response)


def client_observe(addr, path):
    
    host = addr
    client = HelperClient(server=(host, port))
    cmd = "coap://" + host + ":" + str(port) + path
    client.observe(cmd, client_callback)


# ------------ SERVER ---------------- #

class ConfigurationRes(Resource):

    def __init__(self, name="Config Portal", coap_server=None):
        super(ConfigurationRes, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "Basic Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        #config = { "land_id": 4, "node_id": 5}
        #self.payload = "{"\"
        self.payload = "ciao"
        print(self)
        return self

    def render_PUT(self, request):
        msg = request.payload
        addr = str(request)
        addr = addr.split(",")
        addr = addr[0].split("(")
        addr = addr[1].split(",")
        addr = addr[0].replace("\'", "")
        to_print = "received " + str(msg) + " from " + addr
        log.log_info(to_print)
        #TODO inserire add_addr(land_id, node_id, addr)
        #TODO fare l'observing
        self.payload = "config_rqst_ack"
        return self


class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port), False)
        self.add_resource("new_config/", ConfigurationRes())


def listener():

    server = CoAPServer(my_ip, port)

    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")