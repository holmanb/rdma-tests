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

class SwitchInitializationError(Exception):
    """ Provides error if incorrect initialization occurs
    """
    pass

class Switch(Node):
    def __init__(self, ethif=None, available=None, username=None, switch_type=None):
        """ Parent has side effects we don't want
        """
        self.ethif=ethif
        self._available=available
        self.username=username
        self.type = switch_type

        if (not ethif) or (not username) or (not switch_type):
            raise SwitchInitializationError("Need to provide ethif, username and type")

    def print(self):
        """ Prints switch information
        """
        if(self.ethif):
            print(self.ethif.id)
            if self.ethif:
                sys.stdout.write("Ethernet:        ")
                self.ethif.print()

    def whoami(self):
        """ Example of using inherited method.
        """
        return super().command('whoami',username=self.username)

    def reboot(self):
        """ Reboots the switch according to the appropriate commands
        """
        def mlnx():
            """ For rebooting switches that use mlnx-os
            """
            pass

        def nix_like():
            """ For rebooting switches that use *nix-like shutdown commands
            """
            pass

        if self.type == 'mlnx':
            mlnx()
        elif self.type == 'cumulus': 
            nix_like()
            

    def write_file(self):
        """ Example of using inherited method.
        """
        super().command('echo mytext > tmpfile',username=self.username)
