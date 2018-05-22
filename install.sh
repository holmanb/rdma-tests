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

	# Pip and python development package
	sudo yum install python34-pip -y
	sudo yum install python34-devel -y

	# Get non-python paramiko dependencies
	sudo yum install gcc libffi-devel openssl-devel -y

	# install paramiko
	sudo pip3 install paramiko

# for suse
elif [ "$SUSE" -ne -1 ]; then
	
	# Pip and python development package
	sudo zypper install -y python3-pip 
	sudo zypper install -y python3-devel 

	# Get non-python paramiko dependencies
	sudo zypper install -y gcc libffi-devel openssl-devel 

	# install paramiko
    sudo pip3 install --upgrade pip
	sudo pip3 install paramiko

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
echo "export PATH=$PATH:$DIR/interop" >> $HOME/$PERSIST_FILE

# Add network module to PYTHONPATH
echo
echo "persistantly adding network module to PYTHONPATH via ~/.bashrc"
echo "export PYTHONPATH=$PYTHONPATH:$DIR/interop/testlib/classes" >> $HOME/$PERSIST_FILE

# Make the persistant file have correct permissions
chown $SUDO_USER $HOME/$PERSIST_FILE

# Makes current shell work 
echo
echo "start a new shell or run `$ source $HOME/$PERSIST_FILE`  for the environment variables to be available"

# Set up rsa_keys for non-root user
#echo "setting up rsa keys"
#cp /root/.ssh/id_rsa /home/$SUDO_USER/.ssh/
#chown $SUDO_USER /home/$SUDO_USER/.ssh/id_rsa

echo
echo "done!"


