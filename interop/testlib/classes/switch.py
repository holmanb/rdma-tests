try:
    from testlib.classes.node import Node
except Exception as e:
    try:
        # This import path is attempted if the former fails
        # It is used for developers to try network module commands using the Python3 interpreter
        from node import Node
    except Exception as e2:
        raise e

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
