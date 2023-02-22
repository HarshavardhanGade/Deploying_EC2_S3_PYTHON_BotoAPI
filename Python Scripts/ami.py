import boto3

ec2_client = boto3.client('ec2',region_name="us-west-2")

response = ec2_client.describe_images(
    Owners=['099720109477'], # the owner ID for the official Ubuntu AMIs
    Filters=[
        {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*']}
    ]
)

image_id = response['Images'][0]['ImageId']
print(f"AMI ID: {image_id}")
