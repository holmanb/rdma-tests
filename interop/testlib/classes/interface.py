#!/usr/bin/python3


import ipaddress
import nmap

def r_pad(arg, length):
    """ not getting rjust, center, or ljust to work the way I want, so I'm rolling my own
    """
    if length <= len(arg):
        return arg
    else:
        return arg + " " * (length - len(arg))


class Interface:
    def __init__(self, ip=None, header=None, hostname=None, aliases=None):
        """ Represents a node's interface. Stores ipaddr, hostname, etc.
        This gets interface state on intitialization.
        """
        self.id = header or ""
        self.hostname = hostname or ""
        self.aliases = aliases or []
        self.ip = ""
        if ip:
            try:
                self.ip=ipaddress.ip_address(ip)
            except ipaddress.AddressValueError as e:
                print("Error parsing ip address from hosts.conf file")
                raise e
        self.stored_state = None

    def print(self):

        # Formating
        aliases = "\t".join(self.aliases)
        aliases = r_pad(aliases,25)
        hostname =r_pad(self.hostname,30)
        ip = str(self.ip) 
        ip = r_pad(ip,16)
        state=self.stored_state if self.stored_state else "down"
        state = r_pad(state, 10)
        print("{} {} {} {} ".format(ip,hostname, aliases, state))

    def get_state(self):
        """ Use python-nmap to get interface state
        """
        # Only checking port 22, but could check others if needeed
        ip_str = str(self.ip)
        nm = nmap.PortScanner()
        nm.scan(ip_str, '22')

        # Get host state if it is reachable 
        if ip_str in nm.all_hosts():
            self.stored_state = nm[ip_str].state()
            return self.stored_state

        # Otherwise unreachable
        self.stored_state = None
        return "Unreachable"

def validate():
    Interface().print()

if __name__ == "__main__":
    validate()

