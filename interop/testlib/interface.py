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
        try:
            self._ipaddress=ipaddress.ip_address(ip) or ""
        except AddressValueError as e:
            print("Error parsing ip address from /etc/hosts file")
            raise e

    def print_node(self):
        print("{} {} {} {} ".format(self._header, str(self._ipaddress), self._hostname, " ".join(self._aliases)))


