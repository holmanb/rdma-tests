#!/usr/bin/python3

import paramiko
import sys
import ipaddress


class Node:
    def __init__(self, ip=None, header=None, hostname=None, aliases=None):
        """ Represents a node.  Holds certain info and provides functionality for a node
        """
        self._header = header or ""
        self._hostname = hostname or ""
        self._aliases = aliases or []
        self._available = False
        try:
            self._ipaddress =ipaddress.ip_address(ip) or ""
        except AddressValueError as e:
            print("Error parsing ip address from /etc/hosts file")
            raise e

    def print_node(self):
        print("{} {} {} {} ".format(self._header, str(self._ipaddress), self._hostname, " ".join(self._aliases)))


class Network:

    def __init__(self):
        """ Provides common network management functionality
        """
        self._nodes = []


    def add_node(self, node):
        """ Adds new node
        """
        if not isinstance(node,Node):
            raise TypeError
        self._nodes.append(node)

    def get_nodes(self):
        """ Returns the nodes
        """
        return self._nodes

    def load_nodes(self):

        """ Parses /etc/hosts files for node information
        """

        # Parse /etc/hosts
        # Assuming the following layout: 
        # IPAddress  hostname  alias1 alias2 aliasN 
        with open('/etc/hosts') as hostfile:
            section = ''

            for line in hostfile:
                line = line.strip()

                # Just for reference
                if line and line[0] == "#":
                    section = line

                # Ignore blank lines
                elif(not line or (line[0]==':' and line[1]==':')):
                    continue

                else:

                    # Get info from the line for the node 
                    line = line.split()
                    ip = line[0]
                    hostname = line[1]
                    aliases = line[2:]

                    # Create node object and add it to the network object 
                    self.add_node(Node(header=section, ip=ip, hostname=hostname, aliases=aliases))
        return self

def validate():
    Network().load_nodes().get_nodes()

if __name__ == "__main__":
    validate()

