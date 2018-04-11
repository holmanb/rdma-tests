#!/usr/bin/python3

import sys
import paramiko
import subprocess
import shlex
import os

# User defined modules
try:
    # default import for interop.py
    from testlib.classes.subnetmanager import SubnetManager
except Exception as e:
    try:
        # this is in case developers want to import network from an interpreter 
        from subnetmanager import SubnetManager
    except Exception as e2:
        raise e


class Node:
    def __init__(self, sm=None, ibif=None, opaif=None, roceif=None, ethif=None, available=None):
        """ Represents a node"""
        self.ibif = ibif
        self.ethif = ethif
        self.opaif = opaif
        self.roceif = roceif
        self.sm = sm
        self._available=available
        if sm:
            sm.setNode(self)
        if not sm and ethif:
            self.sm = SubnetManager(node=self)


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
        if(self.ethif or self.ibif or self.opaif or self.roceif):
            print("Node: " + self.ethif.id if self.ethif else self.ib.id)
            if self.ethif:
                sys.stdout.write("Ethernet:        ")
                self.ethif.print()
            if self.ibif:
                sys.stdout.write("Infiniband:      ")
                self.ibif.print()
            if self.opaif:
                sys.stdout.write("Omnipath:        ")
                self.opaif.print()
            if self.roceif:
                sys.stdout.write("ROCE:            ")
                self.roceif.print()
        else:
            print("NODE HAS NO INTERFACES?")


        # Print subnet manager info
        sys.stdout.write("Subnet Manager: ")
        self.sm.print()

    def command(self, command, port=22, username='root'):
        """ Executes a single command on the node and returns the output
        """

        # SSH into yourself
        if "master" in self.ethif.id.lower():
            p = subprocess.Popen(shlex.split(command), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = p.communicate()[0].decode('utf-8')
            return output

        # Otherwise go for it
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
            try:
                mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
            except FileNotFoundError as e:
                print("RSA keys need to be setup")
                raise e

            try:
                ssh.connect(str(self.ethif.ip), port=22, username=username, pkey=mykey)
            except Exception as e:
                print("ip:{} port:{} name:{} key:{}".format(self.ethif.ip,22,username,str(mykey)))
                raise e
            stdin, stdout, stderr = ssh.exec_command(command)
            output = "".join(stdout.readlines())
            return output

def validate():
    n=Node()
    n.isUp()
    n.isDown()
    n.isAvailable()
    n.setAvailable(True)
    print(n.command("whoami"))

if __name__ == "__main__":
    validate()
