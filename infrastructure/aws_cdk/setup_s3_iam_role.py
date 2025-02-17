import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

aws_region = "us-east-1"
bucket_name = os.getenv("S3_BUCKET_NAME")


def create_s3_bucket():
    s3_client = boto3.client("s3", region_name=aws_region)
    try:
        print(f"Creating S3 bucket: {bucket_name}")
        s3_client.create_bucket(
            bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": aws_region},
        )
        print(f"S3 bucket: {bucket_name} created")
    except Exception as e:
        print(f"Error in creating S3 bucket: {e}")


def setup_s3_iam_role():
    role_name = "RedshiftServerlessS3Role"
    aws_region = "us-east-1"

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
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*",
                ],
            }
        ],
    }

    iam_client = boto3.client("iam", region_name=aws_region)

    try:
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
            RoleName=role_name,
            PolicyName="S3AcessPolicy",
            PolicyDocument=json.dumps(s3_policy),
        )
        print("IAM Role successfully attached to S3 permissions!")
    except Exception as e:
        print(f"Error in setup S3 IAM role: {e}")
    return role_arn


if __name__ == "__main__":
    create_s3_bucket()
    # setup_s3_iam_role()
