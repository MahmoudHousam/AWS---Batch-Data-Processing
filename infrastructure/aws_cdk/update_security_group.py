import os
import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

aws_region = "us-east-1"
MY_IP = requests.get("https://api64.ipify.org?format=json").json()["ip"] + "/32"
security_group_id = os.getenv["SECURITY_GROUP_ID"]
ec2_client = boto3.client("ec2", region_name=aws_region)


def update_security_group():
    # Update inbound roles to accept requests from the public internet
    try:
        print("Allowing inbound Redshift traffic...")
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 5439,
                    "ToPort": 5439,
                    "IpRanges": [
                        {
                            "CidrIp": MY_IP,
                            "Description": "Allow Redshift access from any IP",
                        }
                    ],
                }
            ],
        )
        print("Security Group updated successfully!")
    except Exception as e:
        print(f"Error in updating security group: {e}")


if __name__ == "__main__":
    update_security_group()
