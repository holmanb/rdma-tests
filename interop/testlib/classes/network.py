#!/usr/bin/python3

import paramiko
import sys
import threading
import os

# User defined modules
try:

    # This import path is used by interop.py (this is the default)
    from testlib.classes.interface import Interface
    from testlib.classes.node import Node
except Exception as e:
    try:
        # This import path is attempted if the former fails
        # It is used for developers to try network module commands using the Python3 interpreter
        from interface import Interface
        from node import Node
    except Exception as e2:

        # The default import path is more important
        raise e


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
    global nodes,self,print_called
    load_nodes()
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
    del nodes[:]
    file_name = os.path.join(os.path.dirname(__file__),'./../../hosts.conf')
    #with open('./../../hosts.conf') as hostfile:
    with open(file_name) as hostfile:
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

                # Filler line in hosts.conf
                if line[0].strip() == "None":
                    continue

                # Each node in the config filestarts with "Node <id>"
                if line[0].upper() == "NODE" or "SWITCH" in "".join(line).upper() :
                    id = line[1]
                    ib = None
                    eth = None
                    opa = None
                    roce = None
                    item = 0
                else:
                    # Each node has 4 or less interfaces
                    if item >= 5:
                        raise NetworkConfigParseError("hosts.conf file is being parsed incorrectly")
                    item +=1

                    # The interface line is like this: ip hostname alias1 alias2 aliasN
                    # Though it typically only has one alias
                    ip = line[0]
                    if len(line) == 1:
                        print(id)
                        print(ip)
                    hostname = line[1]
                    aliases = line[2:]


                    # The first interface line is the ethernet
                    if item == 1:
                        eth = Interface(header=id, ip=ip, hostname=hostname, aliases=aliases)
                    # The second interface line is for infiniband
                    if item == 2:
                        ib = Interface(header=id, ip=ip, hostname=hostname, aliases=aliases)
                    # The third interface line is for opa
                    if item == 3:
                        opa = Interface(header=id, ip=ip, hostname=hostname, aliases=aliases)
                    # The third interface line is for opa
                    if item == 4:
                        roce = Interface(header=id, ip=ip, hostname=hostname, aliases=aliases)

                # Once everything is defined, create and save the node
                if id and eth and ib:
                    add_node(Node(ibif=ib, ethif=eth, opaif=opa, roceif=roce, available=False))

    # scan network for interface status in parrallel
    threads = []
    for node in nodes:
        threads.append(threading.Thread(target=node.ethif.get_state))
        threads.append(threading.Thread(target=node.ibif.get_state))

    # start threads
    for thread in threads:
        thread.start()

    # wait for the threads to finish getting interface status
    for thread in threads:
        thread.join()

    # update SM status now that interfaces are updated
    for node in nodes:
        node.sm.status()

    return self

# Module is initialized
load_nodes()

def validate():
    #n = print_status()
    pass

if __name__ == "__main__":
    validate()

