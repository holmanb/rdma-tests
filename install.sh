# For handling project dependencies
yum install epel-release -y
yum install python34 -y

# Pip and python development package
yum install python34-pip -y
yum install python34-devel -y

# Get non-python paramiko dependencies
yum install gcc libffi-devel openssl-devel -y

# install paramiko
pip3 install paramiko

