import boto3

ec2 = boto3.client('ec2')
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc['Vpc']['VpcId']
ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})

subnet = ec2.create_subnet(CidrBlock='10.0.0.0/24', VpcId=vpc_id)
subnet_id = subnet['Subnet']['SubnetId']

print("VPC and subnet created successfully!")
print(f"VPC ID: {vpc_id}")
print(f"Subnet ID: {subnet_id}")
#print("END")