#!/usr/bin/python3


import ipaddress
import nmap

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
                print("Error parsing ip address from /etc/hosts file")
                raise e
        self.state = None

    def print(self):

        # Formating
        aliases = " ".join(self.aliases)
        aliases = aliases.rjust(30-len(aliases))
        hostname = self.hostname.rjust(30-len(self.hostname))

        print("\t{}\t{}{}\t{} ".format(str(self.ip),hostname, aliases,self.state))

    def get_state(self):
        """ Use python-nmap to get interface state
        """
        # Only checking port 22, but could check others if needeed
        ip_str = str(self.ip)
        nm = nmap.PortScanner()
        nm.scan(ip_str, '22')

        # Get host state if it is reachable 
        if ip_str in nm.all_hosts():
            self.state = nm[ip_str].state()
            return self.state

        # Otherwise unreachable
        return "Unreachable"

def validate():
    Interface().print()

if __name__ == "__main__":
    validate()

