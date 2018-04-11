from node import Node

import sys

class Switch(Node):
    def __init__(self, ethif=None, available=None):
        """ Parent has side effects we don't wand
        """
        self.ethif=ethif
        self._available=None

    def print(self):
        """ Prints switch information
        """
        if(self.ethif):
            print(self.ethif.id)
            if self.ethif:
                sys.stdout.write("Ethernet:        ")
                self.ethif.print()
