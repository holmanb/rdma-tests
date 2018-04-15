#!/usr/bin/python3

import sys
import paramiko
import subprocess
import shlex
import os

# import user defined modules
try:
    # default import for interop.py
    from testlib.classes.subnetmanager import SubnetManager
except Exception as e:
    try:
        # this is in case developers want to import network from an interpreter 
        from subnetmanager import SubnetManager
    except Exception as e2:
        raise e

class RSAKeySetupError(Exception):
    pass

class Node:
    def __init__(self, sm=None, ibif=None, opaif=None, roceif=None, ethif=None, available=None):
        """ Represents a node"""
        self.ibif = ibif
        self.ethif = ethif
        self.opaif = opaif
        self.roceif = roceif
        self.sm = sm
        self._available=available
        if not sm:
            self.sm = SubnetManager(node=self)

    def set_interface(self, ibif=None, opaif=None,roceif=None, ethif=None):

        if ibif:
            if(self.ibif):
               sys.stderr.write("Reassigning ibif interface {} to {}\n".format(self.ibif.id, ibif.id))
            self.ibif = ibif
        if ethif:
            if(self.ethif):
               sys.stderr.write("Reassigning ethif interface {} to {}\n".format(self.ethif.id, ethif.id))
            self.ethif = ethif
        if opaif:
            if(self.opaif):
               sys.stderr.write("Reassigning opa interface {} to {}\n".format(self.opaif.id, opaif.id))
            self.opaif = opaif
        if roceif:
            if(self.roceif):
               sys.stderr.write("Reassigning roce interface {} to {}\n".format(self.roceif.id, roceif.id))
            self.roceif = roceif

    def is_up(self):
        """ True if management interface is on the network
        """
        return self.ethif.stored_state == "up"


    def is_down(self):
        """ True if node is NOT on the network
        """
        return not self.is_up()

    def is_available(self):
        """ True if node is available for use.
        """
        return self._available

    def set_available(self, bool):
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
            sys.stdout.write("Name:            ")
            print(self.ethif.id if self.ethif else self.ib.id)
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

        # don't want to SSH into yourself, just use the subprocess builtin
        #print(str(self.ethif.id))
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
                raise RSAKeySetupError("RSA keys need to be setup")

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
