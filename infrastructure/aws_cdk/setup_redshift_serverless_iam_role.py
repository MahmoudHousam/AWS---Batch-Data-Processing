import boto3
import json
from policies.redshift_policy import redshift_policy

aws_region = "us-east-1"
iam_client = boto3.client("iam", region_name=aws_region)
role_name = "GitHubActionsRedshiftRole"

# GitHub Actions OIDC
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:MahmoudHousam/batch_data_processing:*"
                }
            },
        }
    ],
}


def create_iam_role():
    try:
        print(f"Creating IAM role: {role_name}")
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="IAM role for GitHub Actions to access Redshift Serverless",
        )
        role_arn = response["Role"]["Arn"]
        print(f"IAM role created successfully: {role_arn}")

        print("Attaching policy to the role...")
        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName="RedshiftServerlessFullAccess",
            PolicyDocument=json.dumps(redshift_policy),
        )
        print("Policy attached successfully.")

        return role_arn
    except Exception as e:
        print(f"Error creating IAM role: {e}")
        return None


if __name__ == "__main__":
    role_arn = create_iam_role()
