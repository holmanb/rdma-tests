#!/usr/bin/python3

import paramiko
import sys
from interface import Interface
from node import Node

class NetworkConfigParseError(Exception):
    """ Custom exception is thrown when a bad config file is parsed"""
    pass

class Network:

    def __init__(self):
        """ Provides common network management functionality
        """
        self.nodes = []

    def print_status(self):
        """ Print the networ status
        """
        for node in self.nodes:
            print("--")
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
                        self.add_node(Node(ibif=ib, ethif=eth, available=False))

        return self

def validate():
    n=Network()
    n.load_nodes().get_nodes()
    n.print_status()

if __name__ == "__main__":
    validate()

