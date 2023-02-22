import boto3

ec2_client = boto3.client('ec2',region_name="us-west-2")

# get the public IP address of the EC2 instance
instance_id = "i-0eb4747be394468ea"
response = ec2_client.describe_instances(InstanceIds=[instance_id])
public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
print(public_ip)
# use SSH to connect to the EC2 instance and install Nginx
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(public_ip, username="ubuntu",key_filename="C:/Users/DELL/Downloads/python_keypair.pem")

stdin, stdout, stderr = ssh.exec_command("sudo apt-get update")
print(stdout.read().decode())

stdin, stdout, stderr = ssh.exec_command("sudo apt-get install nginx -y")
print(stdout.read().decode())

ssh.close()

print("Nginx installed successfully on the EC2 instance!")