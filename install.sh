# For handling project dependencies
yum install epel-release -y
yum install python34 -y

# Pip and python development package
yum install python-pip
yum install python-devel

# Get non-python paramiko dependencies
yum install gcc libffi-devel openssl-devel -y

# install paramiko
pip install paramiko

