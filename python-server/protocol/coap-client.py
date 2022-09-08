import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

host = "127.0.0.1"
port = 5683

path="/hello"

client = HelperClient(server=(host, port))

response = client.get(path)
print(response.pretty_print())
client.stop()
