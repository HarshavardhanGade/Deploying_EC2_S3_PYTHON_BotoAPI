# Deploying an EC2 Instance and S3 Static Website using Python and Boto API

To deploy an EC2 instance, build a VPC and subnet, construct an S3 bucket, and deploy a static website to that bucket, these projects offer Python scripts that uses Boto API. To remotely install Ngnix in the newly formed EC2 instance, another Python script is used.

## Objectives

1. 	Create a VPC and Subnet
2.	Deploy an EC2 instance and attach it to the subnet
3.	Create an S3 bucket and deploy a static website (hello world) using Python
4.	Install Nginx in the EC2 instance using remote execution

## Installation

To use the scripts you will need to install the following dependencies:

i) Python 3.6
ii) Boto3 
iii) awscli

You can use the following command to install the Boto3 and awscli:
pip install boto3
pip install awscli

-> The following steps need to be followed Before starting the process:

1. Craete a root user account https://aws.amazon.com/resources/create-account/
2. Install all the required libraries.
3. Create a IAM(Identity and Access Management) user in your AWS account
- Search for IAM
- On left pane click on "users"
- click on "Add users"
- Give a name for user and click "next"
- In "Set Permissions" page click on "Attach policies directly(this is used to add only required permission policies")
- Scroll Down add these two permissions "Administrator Access" and "AmazonEC2FulAccess" and click "Next"
- click "create user"
That's it! IAM user is successfully created.
4. Now, click on the user that you have created and scroll down and goto "Security Credentials".
5. Click on "Create Access key" and select "Command Line interface" and click "Next".
6. Click "create access key" after adding any description(optional).
7. Access Key and Secret Access key will be craeted. Download the ".csv" file (contains keys).
8. Go to Command Prompt and run command "aws configure"
9. Enter the accesss key and Secret access key with default region(in this case i have used "us-west-2") and leave other option Default output and click Enter
10. If you not wish to use qws configure then you need to mention access keys direclty in the scripts but it may produce security issues.

## APPROACH AND CODING PROCESS

## Need to create Virtual Private CLoud(VPC) -- vpc.py

- Code strats with importing boto3 which is used for communication with AWS Services

- An EC2 client can be created by typing ec2 = boto3.client('ec2') and using it to interface with EC2 instances, VPCs, subnets, and other related AWS services.

- A new VPC with the supplied CIDR(Classless Inter-Domain Routing) block of IP addresses is created with the command vpc = ec2.create vpc(CidrBlock='10.0.0.0/16'). The IP address range that can be utilised inside the VPC is determined by the CIDR block. The CIDR block is now configured to "10.0.0.0/16" in this instance.

- The response object returned by the create vpc() method's ['VpcId'] function extracts the ID of the newly established VPC.

- DNS support is enabled for the VPC using ec2.modify vpc attribute(VpcId=vpc id, EnableDnsSupport='Value': True), which permits instances inside the VPC to resolve domain names.

- When DNS hostnames are enabled for the VPC, which is done with ec2.modify vpc attribute(VpcId=vpc id, EnableDnsHostnames='Value': True), instances inside the VPC can have fully qualified domain names.

- A new subnet is created inside the VPC using the command subnet = ec2.create subnet(CidrBlock='10.0.0.0/24', VpcId=vpc id). The subnet's CIDR block is set to "10.0.0.0/24" and it is connected to the VPC using the VpcId option.

- The response object returned by the create subnet() method's ['SubnetId'] function extracts the ID of the just formed subnet.

- The last tw lines just print a successfulr message with ID's of VPC and subnet.

## Need to get AMI(Amazon Machine Image) ID -- ami.py (or we can also find in the AWS console)

- creates an ec2 client
- ec2 client is the response. describe images(...) invokes the EC2 client's describe images() method, which provides details about the Amazon images that are currently accessible. The owner of the images is identified by their ID in the Owners parameter, which in this case is the legitimate owner of the Ubuntu AMI. The filters to be applied to the image results are specified by the Filters parameter. The filter in this instance looks for AMIs with names that begin with "ubuntu-bionic-18.04-amd64-server-," which denotes the most recent iteration of the recognised Ubuntu AMI for the specified area.

- The describe images() response's ['ImageId'] field pulls the ID of the most recent Ubuntu AMI. Launching EC2 instances with the supplied Ubuntu AMI requires the ID.
- The last line prints the AMI ID that is retrieved.

## Creating EC2 instance and Attaching subnetID to it. --ec2.py
 Before starting the code 
 we need to create an KeyPair in AWS you can just search KeyPairs and create it.Also Download the key pair in the form of ".pem" extension and select type as "RSA".
 KeyPairs contains a public key and private key.
 
 - A key pair is used in Amazon EC2 to securely SSH into an instance. You must designate a key pair when you launch an instance. The SSH connection to the instance is authenticated using the key pair.
 
 Approach:
 
 - craete an EC2 client using resource() method instead of client() (this is just to access high level interfaces)
 
 - store subnetID and amiID in a variable

- EC2 instances are created using the supplied parameters when instance = ec2.create instances(...) is used. The ID of the AMI to use is specified by the ImageId option. The instance type, in this example t2.micro, is specified by the InstanceType parameter. The name of the key pair used to authenticate SSH access to the instance is specified by the KeyName argument. The subnet to launch the instance in and whether to give the instance a public IP address are both specified by the NetworkInterfaces argument. The name tag for the instance is specified by the TagSpecifications parameter.

- instance[0].instance_id is used to retrieve the instance
 ID
 
 - The last line prints the Instance ID that os retrieved
 
 ## Creating S3 and Deploying a static website in it. -- bucket.py
 
 - create a S3 client
 
 - The new bucket's name and region are set as bucket name and region, respectively.

- With the given parameters, s3.create bucket(...) creates a new S3 bucket. The CreateBucketConfiguration parameter sets the region of the bucket, and the Bucket parameter specifies the name of the bucket.

- A file is uploaded to the new bucket using s3.put_object(...). The Key parameter specifies the name of the file, and the Bucket parameter specifies the name of the bucket to upload to. The file's contents are specified by the Body argument, and its MIME(Multipurpose Internet Mail Extension) type is specified by the ContentType parameter.

- Body parameter in the put_objeect is where the html code has written.

- The last line prints a successfull message indicating the website has successfully deployed in S3 bucket

Note:- The bucket name should not contain any uppercase letters or special characters and need to be unique

## Installing Nginx Remotely through Python -- nginx.py

- The ID of the EC2 instance that we wish to connect to is set in instance id.

- Get the IP address of the instance by defining its attributes using response = ec2 client.describe_instances(InstanceIds=[instance id]).

- The EC2 instance's public IP address is specified as public_ip.

- The creation of an SSH client makes use of the paramiko library.(no need of any installation for using this library)

- The EC2 instance's host key is automatically added to the known hosts file by the SSH client when ssh.set missing host key policy(paramiko.AutoAddPolicy()) is called.

- With the given arguments, ssh.connect(public ip, username="ubuntu", key filename="C:/Users/DELL/Downloads/python_keypair.pem") creates an SSH connection to the EC2 instance.

- SSH connection is used to run the command sudo apt-get update on the EC2 instance using the following syntax: stdin, stdout, stderr = ssh.exec command("sudo apt-get update").
- print(stdout.read().decode()) displays the successful installation of Nginx.

- ssh.close() closes the connection

- The last line prints a sucessfull message of Nginx intsllation.

NOTE:- The above script may produce a connection establishment error and the following are two solutions to avoid it.

1. In AWS Management Console, goto VPC>subnets>click on your subnet>Route Table>click on the Route table ID >Edit Route Table>Add Route>0:0:0:0/0 and Target as instance>click save
Also add another Route ::/0 with Traget as instance.
Again repeat the above steps with chamge in target as internet Gateway.

2. In AWS Management Console, goto System Manager>Session Manager>Create a session using IAM user.

The above solutions may solve the problem if occured:)

## Challenges I faced while doing this project:

I have faced a few difficulties in putting this project into practise, which needed more reserach and problem-solving.
The following are some of the difficulties: 
- Setting up the security groups and network settings to permit access to the EC2 instance and S3 bucket
- Troubleshooting Boto API and AWS SDK for Python code errors; 
- Making sure the S3 website was reachable from the internet and set up with the appropriate permissions.
Nonetheless, I  able to overcome these difficulties and successfully install the EC2 instance and S3 website with the aid of the AWS documentation and community forums.
References: https://realpython.com/python-boto3-aws-s3/

## Outcomes

- Gained hands-on experience with Amazon Web Services (AWS) and learned how to interact with AWS services using Python and the boto3 library.
- Learned how to create and configure VPCs, subnets, and EC2 instances in AWS using Python and boto3.
- Learned how to create and manage S3 buckets and deploy static websites in AWS using Python and boto3.
- Learned how to automate the deployment and configuration of software on EC2 instances using remote execution and Python.
- Developed skills in writing clean, well-structured Python code that interacts with AWS services using the boto3 library

## Conclusion

In this project, I've shown how to deploy an EC2 instance and a static S3 website using Python and the Boto API, as well as how to remotely execute Nginx installation on the EC2 instance. The deployment of web apps or other cloud services in AWS can be automated using this.

NOTE:- Make sure to keep all the python scripts in the same directory :)

Static Website URL: https://harshabucketpython134.s3.us-west-2.amazonaws.com/index.html [REMOVED]

Please also note that I have done above tasks in separate files make sure to use the outputs generated by one in another file. Also take care of variables:) 
(Example: subnet id which is generated in vpc.py I have used the same id in ec2.py script).  
