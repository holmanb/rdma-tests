#!/usr/bin/python3

import re

class SubnetManagerInitializationError(Exception):
    """ Custom initialization exception
    """
    pass

class SubnetManagerParsingError(Exception):
    """ In case the subnet manager output is parsed incorrectly
    """
    pass

class SubnetManager:
    def __init__(self, node=None):
        """ Represents the subnet manager
        """
        self.ip = node.ethif.ip
        self.node = node
        if not self.ip or not self.node:
            raise SubnetManagerInitializationError("Must initialize SubnetManager object with node")
        self.stored_state = self.status()

    def start(self):
        """ Starts the subnet manager at ip address
        """
        if self.node.is_up():
            self.node.command("systemctl start opensm")
            return True
        else:
            return False

    def stop(self):
        """ Stop the subnet manager at ip address
        """
        if self.node.is_up():
            self.node.command("systemctl stop opensm")
            return True
        else:
            return False

    def status(self):
        """ Status of the subnet manager at the ip address
        """
        if self.node.is_up():
            # opensm for status
            output = self.node.command("systemctl status opensm")
            active_lines = []
            for line in output.split('\n'):
                if "Active: " in line:
                    active_lines.append(line)
            if len(active_lines) != 1:
                raise SubnetManagerParsingError("the output of `systemctl status opensm` was parsed incorrectly")
            else:
                self.state = active_lines[0].strip().split()[1]
                return self.state
        return False

    def print(self):
        """ Print the the subnet manager status
        """
        print("Untracked" if not self.stored_state else self.stored_state)

def validate():
    SubnetManager().print()

if __name__ == "__main__":
    validate()

