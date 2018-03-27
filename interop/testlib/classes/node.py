#!/usr/bin/python3

from subnetmanager import SubnetManager
import sys

class Node:
    def __init__(self, sm=None, ibif=None, ethif=None, available=None):
        """ Represents a node"""
        self.ibif = ibif
        self.ethif = ethif
        self.sm = sm
        if not sm and ethif:
            self.sm = SubnetManager(ethif.ip)

        self._available=available

    def isUp(self):
        """ True if node is on the network
        """
        pass

    def isDown(self):
        """ True if node is NOT on the network
        """
        pass

    def isAvailable(self):
        """ True if node is available for use.
        """
        return self._available

    def setAvailable(self, bool):
        """ Set availability of the node
        """
        if bool is True:
            self._available=True

        elif bool is False:
            self._available=False

        else:
            raise TypeError

    def print(self):
        """ Prints node information
        """
        if(self.ethif or self.ibif):
            print("Node: " + self.ethif.id if self.ethif else self.ib.id)
            if self.ethif:
                sys.stdout.write("Ethernet:  ")
                self.ethif.print()
            else:
                sys.stdout.write("Ethernet: None\n")
            if self.ibif:
                sys.stdout.write("Infiniband: ")
                self.ibif.print()
            else:
                sys.stdout.write("Infiniband: None\n")
        else:
            print("NODE HAS NO INTERFACES?")

        # Print subnet manager info
        self.sm.print()

    def command(self):
        """ Executes a single command on the node and returns the output
        """
        pass 

def validate():
    n=Node()
    n.isUp()
    n.isDown()
    n.isAvailable()
    n.setAvailable(True)

if __name__ == "__main__":
    validate()
