#!/usr/bin/python3

import paramiko
import sys
from interface import Interface
from node import Node

class Network:

    def __init__(self):
        """ Provides common network management functionality
        """
        self.nodes = []

    def print_status(self):
        """ Print the networ status
        """
        for node in self.nodes:
            node.print()

    def add_node(self, node):
        """ Adds new node
        """
        if not isinstance(node, Node):
            raise TypeError
        self.nodes.append(node)

    def get_nodes(self):
        """ Returns the nodes
        """
        return self.nodes

    def load_nodes(self):

        """ Parses /etc/hosts files for node information
        """

        # Parse /etc/hosts
        # Assuming the following layout: 
        # IPAddress  hostname  alias1 alias2 aliasN 
        with open('/etc/hosts') as hostfile:
            section = ''
            interfaces = []
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
                    interfaces.append(Interface(header=section, ip=ip, hostname=hostname, aliases=aliases))

                # Pairing up interfaces into nodes
                ib = None
                eth = None
                for i in range(int(len(interfaces)/2)):
                    for interface in interfaces:
                        for alias in interface.aliases:
                            print(alias)
                            moniker = "ofa-node{}"
                            if moniker.format(i) in alias:

                                if moniker.format(i) + '-ib0' in alias:
                                    ib=interface
                                else:
                                    eth=interface
                    self.add_node(Node(ibif=ib, ethif=eth, available=False))

        return self

def validate():
    n=Network()
    n.load_nodes().get_nodes()
    n.print_status()

if __name__ == "__main__":
    validate()

