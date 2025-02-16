import os
import boto3

aws_region = "us-east-1"
security_group_id = os.environ["SECURITY_GROUP_ID"]
ec2_client = boto3.client("ec2", region_name=aws_region)

# Update inbound roles to accept requests from the public internet
print("Allowing inbound Redshift traffic...")
ec2_client.authorize_security_group_ingress(
    GroupId=security_group_id,
    InPermissions=[
        {
            "IpProtocol": "tcp",
            "FromPort": 5439,
            "ToPort": 5439,
            "IpRanges": [
                {
                    "CidrIp": "0.0.0.0/0",
                    "Description": "Allow Redshift access from any IP",
                }
            ],
        }
    ],
)
print("✅ Security Group updated successfully!")
