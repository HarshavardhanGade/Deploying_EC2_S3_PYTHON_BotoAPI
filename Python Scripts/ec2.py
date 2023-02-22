import boto3

ec2 = boto3.resource('ec2',region_name="us-west-2")
subnet_id = "subnet-02353173950f10872"
ami_id = "ami-09d50d5363fe58c51"

instance = ec2.create_instances(
    ImageId=ami_id,
    InstanceType='t2.micro',
    KeyName="python_keypair",
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[
        {
            'SubnetId': subnet_id,
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
        }
    ],
    TagSpecifications=[
        {
        'ResourceType': 'instance',
        'Tags': [
            {
                'Key': 'Name',
                'Value': 'harsha_ec2_2'
            },
        ]
    }]
)
instance_id = instance[0].instance_id
print(f"EC2 instance created successfully with ID: {instance_id}")
print("END")
