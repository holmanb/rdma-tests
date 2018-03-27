#!/usr/bin/python3

class SubnetManager:
    def __init__(self, ip=None):
        """ Represents the subnet manager
        """
        self.ip=ip
        self.status=None

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
        pass

    def print(self):
        """ Print the the subnet manager status
        """
        print("Subnet Manager: {}".format("Untracked" if not self.status else self.status))

def validate():
    SubnetManager().print()

if __name__ == "__main__":
    validate()

