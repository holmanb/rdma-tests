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
