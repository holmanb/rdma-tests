#!/usr/bin/python3


import ipaddress

class Interface:
    def __init__(self, ip=None, header=None, hostname=None, aliases=None):
        """ Represents a node.  Holds certain info and provides functionality for a node
        """
        self.header = header or ""
        self.hostname = hostname or ""
        self.aliases = aliases or []
        self.available = False
        if ip:
            try:
                self.ip=ipaddress.ip_address(ip) 
            except ipaddress.AddressValueError as e:
                print("Error parsing ip address from /etc/hosts file")
                raise e
        else:
            self.ip = ""

    def print(self):
        print("{} {} {} {} ".format(self.header, str(self.ip), self.hostname, " ".join(self.aliases)))

def validate():
    Interface().print()

if __name__ == "__main__":
    validate()
