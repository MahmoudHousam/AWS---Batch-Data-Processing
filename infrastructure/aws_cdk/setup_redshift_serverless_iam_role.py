import boto3
import json

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

redshift_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "redshift:*",
                "redshift-serverless:*",
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeAddresses",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:DescribeInternetGateways",
                "ec2:AuthorizeSecurityGroupIngress",
                "sns:CreateTopic",
                "sns:Get*",
                "sns:List*",
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "cloudwatch:PutMetricAlarm",
                "cloudwatch:EnableAlarmActions",
                "cloudwatch:DisableAlarmActions",
                "tag:GetResources",
                "tag:UntagResources",
                "tag:GetTagValues",
                "tag:GetTagKeys",
                "tag:TagResources",
            ],
            "Effect": "Allow",
            "Resource": "*",
        },
        {
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "arn:aws:iam::*:role/aws-service-role/redshift.amazonaws.com/AWSServiceRoleForRedshift",
            "Condition": {
                "StringLike": {"iam:AWSServiceName": "redshift.amazonaws.com"}
            },
        },
        {
            "Sid": "DataAPIPermissions",
            "Action": [
                "redshift-data:ExecuteStatement",
                "redshift-data:CancelStatement",
                "redshift-data:ListStatements",
                "redshift-data:GetStatementResult",
                "redshift-data:DescribeStatement",
                "redshift-data:ListDatabases",
                "redshift-data:ListSchemas",
                "redshift-data:ListTables",
                "redshift-data:DescribeTable",
            ],
            "Effect": "Allow",
            "Resource": "*",
        },
        {
            "Sid": "SecretsManagerListPermissions",
            "Action": ["secretsmanager:ListSecrets"],
            "Effect": "Allow",
            "Resource": "*",
        },
        {
            "Sid": "SecretsManagerCreateGetPermissions",
            "Action": [
                "secretsmanager:CreateSecret",
                "secretsmanager:GetSecretValue",
                "secretsmanager:TagResource",
            ],
            "Effect": "Allow",
            "Resource": "*",
            "Condition": {
                "StringLike": {"secretsmanager:ResourceTag/RedshiftDataFullAccess": "*"}
            },
        },
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
