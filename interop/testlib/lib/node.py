#!/usr/bin/python3

from subnetmanager import SubnetManager

class Node:
    def __init__(self, sm=None, ibif=None, ethif=None, available=None):
        """ Represents a node"""
        self.ibif=ibif
        self.ethif=ethif
        self.sm=sm
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
        print("NODE")
        self.ethif.print()
        self.ibif.print()


def validate():
    n=Node()
    n.isUp()
    n.isDown()
    n.isAvailable()
    n.setAvailable(True)

if __name__ == "__main__":
    validate()
