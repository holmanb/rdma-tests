
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
	sudo zypper -y install gcc libffi-devel openssl-devel 

	# install paramiko
    sudo pip3 install --upgrade pip
	sudo pip3 install paramiko
	sudo pip3 install python-nmap

fi
