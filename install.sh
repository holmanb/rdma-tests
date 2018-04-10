#!/bin/bash

# Require root
if [[ $EUID -ne 0 ]]; then
    echo "must be root"
    exit 1
fi


# Returns -1 if not subset
strindex() {
	x="${1%%$2*}"
	[[ "$x" = "$1" ]] && echo -1 || echo "${#x}"
}

# get os-type to select multiple package managers
ID_LIKE=`awk -F= '/^ID_LIKE/{print $2}' /etc/os-release`

RHEL=`strindex "$ID_LIKE" 'rhel'`
SUSE=`strindex "$ID_LIKE" 'suse'`

# centos/rhel
if [ "$RHEL" -ne -1 ]; then
		
	# For handling project dependencies
	sudo yum install epel-release -y
	sudo yum install python34 -y
	sudo yum install nmap -y

	# Pip and python development package
	sudo yum install python34-pip -y
	sudo yum install python34-devel -y

	# Get non-python paramiko dependencies
	sudo yum install gcc libffi-devel openssl-devel -y

	# install paramiko
	sudo pip3 install paramiko
	sudo pip3 install python-nmap

# for suse
elif [ "$SUSE" -ne -1 ]; then
	
	# Pip and python development package
	sudo zypper install -y python3-pip 
	sudo zypper install -y python3-devel 
	sudo zypper install -y nmap 

	# Get non-python paramiko dependencies
	sudo zypper install -y gcc libffi-devel openssl-devel 

	# install paramiko
    sudo pip3 install --upgrade pip
	sudo pip3 install paramiko
	sudo pip3 install python-nmap

fi

# So users don't need to use root 
echo
echo "adding permissions to interop.py"
chown root interop/interop.py
chgrp root interop/interop.py
chmod 4775 interop/interop.py

# Get directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Add interop.py to path
PERSIST_FILE=".bashrc"
echo
echo "persistantly adding interop.py to PATH via ~/.bashrc"
echo "export PATH=$PATH:$DIR/interop" >> /home/$SUDO_USER/$PERSIST_FILE

# Add network module to PYTHONPATH
echo
echo "persistantly adding network module to PYTHONPATH via ~/.bashrc"
echo "export PYTHONPATH=$PYTHONPATH:$DIR/interop/testlib/classes" >> /home/$SUDO_USER/$PERSIST_FILE

# Make .profile have correct permissions
chown $SUDO_USER /home/$SUDO_USER/$PERSIST_FILE
chgrp $SUDO_USER /home/$SUDO_USER/$PERSIST_FILE

# Makes current shell work 
echo
echo "exporting PATH and PYTHONPATH to current shell"
export PATH=$PATH:$DIR/interop
export PYTHONPATH=$PYTHONPATH:$DIR/interop/testlib/classes

# Set up rsa_keys
echo "setting up rsa keys"
cp /root/.ssh/id_rsa /home/$SUDO_USER/.ssh/
chown $SUDO_USER /home/$SUDO_USER/.ssh/id_rsa

echo
echo "done!"


