import boto3
import json


aws_region = "us-east-1"
role_name = "RedshiftServerlessS3Role"

# Define the IAM trust ploicy to allow Redshift to assume the role
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "redshift.amazonaws.com"},
            "Action": "sts.AssumeRole",
        }
    ],
}

# Define the IAM plocy to all access to all S3 buckets
s3_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3.GetObject", "s3.PutObject", "s3.ListBucket"],
            "Resouce": ["arn:aws:s3:::*"],
        }
    ],
}

iam_client = boto3.client("iam", region_name=aws_region)

# Create the IAM Role
print("Creating IAM Role for Redshift Serverless...")
role_response = iam_client.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(trust_policy),
    Description="IAM Role for Redshift Serverless to access S3",
)
role_arn = role_response["Role"]["Arn"]
print(f"IAM Role created successfully: {role_arn}")

# Attach S3 Policy to the Role
policy_response = iam_client.put_role_policy(
    RoleName=role_name, PolicyName="S3AcessPolicy", PolicyDocument=json.dumps(s3_policy)
)
print("IAM Role successfully attached to S3 permissions!")
