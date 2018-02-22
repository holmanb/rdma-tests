# For handling project dependencies
yum install epel-release -y
yum install python34 -y

# Pip and paramiko
curl -O https://bootstrap.pypa.io/get-pip.py
/usr/bin/python3.4 get-pip.py

yum install gcc libffi-devel python-devel openssl-devel -y


