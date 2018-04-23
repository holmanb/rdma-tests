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

            # Rebooting the switch requires these two 
            # commands to be called in succession
            command1 = 'enable'
            command2 = 'reload'
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
            try:
                mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
            except FileNotFoundError as e:
                raise RSAKeySetupError("RSA keys need to be setup")
            
            try:
                o=[]
                ssh.connect(str(self.ethif.ip), port=22, username=username, pkey=mykey)
                stdin, stdout, stderr = ssh.exec_command(command1)
                stdin, stdout, stderr = ssh.exec_command(command2)
                output = "".join(stdout.readlines())
                stderr_output = "".join(stderr.readlines()) 
                if not output:
                    output = ""
                if not stderr_output:
                    stderr_output = ""

                # Return values is stdout = o[0], stderr = o[1]
                o = [output, stderr_output]

            except Exception as e:
                print("ip:{} port:{} name:{} key:{}".format(self.ethif.ip,22,username,str(mykey)))
                raise e
            finally:
                ssh.close()
                return o 
            pass
            

        def nix_like():
            """ For rebooting switches that use *nix-like shutdown commands
            """
            super().command('reboot -h now',username=self.username)
            

        if self.type == 'mlnx':
            mlnx()
        elif self.type == 'cumulus': 
            nix_like()
            

    def write_file(self):
        """ Example of using inherited method.
        """
        super().command('echo mytext > tmpfile',username=self.username)
