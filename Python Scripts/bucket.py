import boto3

s3 = boto3.client('s3')

bucket_name = "harshabucketpython134"
region = "us-west-2"

s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': region
    }
)

s3.put_object(
    Bucket=bucket_name,
    Key='index.html',
    Body=b'<html><body><h1>Hello World!</h1></body></html>',
    ContentType='text/html'
)

print("Static website deployed successfully on S3!")