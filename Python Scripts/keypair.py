import boto3
# used this script just for available Keypairs in AWS 
ec2 = boto3.client('ec2',region_name="us-west-2")

response = ec2.describe_key_pairs()
#print(response)
for key_pair in response['KeyPairs']:
    print(key_pair['KeyName'])
