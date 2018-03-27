#!/usr/bin/python3

import re

class SubnetManagerInitializationError(Exception):
    """ Custom initialization exception
    """
    pass

class SubnetManager:
    def __init__(self, node=None):
        """ Represents the subnet manager
        """
        self.ip = node.ethif.ip
        self.node = node
        self.last_status = None
        if not self.ip or not self.node:
            raise SubnetManagerInitializationError("Must initialize SubnetManager object with node") 
        self.status = self.status()

    def start(self):
        """ Starts the subnet manager at ip address
        """
        pass

    def stop(self):
        """ Stop the subnet manager at ip address
        """
        pass

    def status(self):
        """ Status of the subnet manager at the ip address
        """

        # opensm for status
        output = self.node.command("systemctl status opensm")
        print(output)
        return output

    def print(self):
        """ Print the the subnet manager status
        """
        print("Subnet Manager: {}".format("Untracked" if not self.status else self.status))

def validate():
    SubnetManager().print()

if __name__ == "__main__":
    validate()

