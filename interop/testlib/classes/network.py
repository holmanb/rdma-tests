#!/usr/bin/python3

import paramiko
import sys
from interface import Interface
from node import Node

class NetworkConfigParseError(Exception):
    """ Custom exception is thrown when an incorrect config file is parsed"""
    pass

# This allows self-reference within the module
self = sys.modules[__name__]

# Modules are only imported once then cached, so this will not be 
# re-initiallized every time it is imported
nodes = []

##
# Provides common network management functionality
## 
def print_status():
    """ Print the network status
    """
    global nodes,self
    for node in nodes:
        print("--")
        node.print()
    return self

def add_node(node):
    """ Adds new node
    """
    global nodes,self
    if not isinstance(node, Node):
        raise TypeError
    nodes.append(node)
    return self

def load_nodes():

    """ Parses config file for node information
    """

    # Assuming the following layout: 
    # IPAddress  hostname  alias1 alias2 aliasN 
    global nodes, self
    with open('../../hosts.conf') as hostfile:
        item = 0
        ib = None
        eth = None
        for line in hostfile:
            line = line.strip()

            # Skip blank and commented lines
            if not line or line[0] == "#":
                continue
            else:

                # Get info from the line for the node 
                line = line.split()

                # Each node in the config filestarts with "Node <id>"
                if line[0].upper() == "NODE":
                    id = line[1]
                    ib = None
                    eth = None
                    item = 0
                else:
                    # Each node has 2 interfaces
                    if item >= 2:
                        raise NetworkConfigParseError("hosts.conf file is being parsed incorrectly")
                    item +=1

                    # The interface line is like this: ip hostname alias1 alias2 aliasN
                    # Though it typically only has one alias
                    ip = line[0]
                    hostname = line[1]
                    aliases = line[2:]

                    # The first interface line is the ethernet
                    if item == 1:
                        eth = Interface(header=id, ip=ip, hostname=hostname, aliases=aliases)
                    # The second interface line is for infiniband
                    if item == 2:
                        ib = Interface(header=id, ip=ip, hostname=hostname, aliases=aliases)

                # Once everything is defined, create and save the node
                if id and eth and ib:
                    add_node(Node(ibif=ib, ethif=eth, available=False))
        return self

# Module is initialized
load_nodes()

def validate():
    n = load_nodes()
    n = print_status()

if __name__ == "__main__":
    validate()

