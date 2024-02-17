# Manually Create an EC2

## Key Pair

<img src="../../../../../Library/Application Support/typora-user-images/image-20231030231616535.png" alt="image-20231030231616535" style="zoom:50%;" />

1. Create a new key pair for your self.

2. Select .pem file as identity file.

## Network Setting

You could select an existing security group. In this project, we should allow SSH, HTTPs and HTTP trafic from the internet.

Create a security group. 

Allow SSH traffic from, HTTPS and HTTP.

## Select AZ

Select a subnet under the network settings.
<img src="../../../../../Library/Application Support/typora-user-images/image-20231030231957446.png" alt="image-20231030231957446" style="zoom:50%;" />

## User Data

Add the instructions that you want instance to execute when it is launched for the first time.

```shell
#!/bin/bash
yum update -y
yum install git -y
yum install python3 -y
sudo yum install -y python-pip
sudo pip install httpx numpy pandas scipy matplotlib ccxt
sudo pip install urllib3 --upgrade
```



# Manually SSH to an Instance

1. Open ssh config file, add the following content

```txt
Host <Any Text>
  HostName <public ip>
  User ec2-user
  IdentityFile <path of .pem file>
```

2. Update permission to owner only

```shell
chmod 0400 <path of .pem file>
```

When instances restart, need to change public ip.

