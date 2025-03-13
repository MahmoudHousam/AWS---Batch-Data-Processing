import os
import boto3
from dotenv import load_dotenv
from setup_s3_iam_role import role_name

load_dotenv()


def setup_redshift():
    aws_region = "us-east-1"
    workgroup = "brain-tumor-workgroup"
    namespace = "brain-tumor-namespace"
    database_name = "dev_db"
    admin_username = "admin"
    admin_password = os.getenv("ADMIN_PASSWORD")
    redshift_client = boto3.client("redshift-serverless", region_name=aws_region)
    # Fetch the role ARN
    iam_client = boto3.client("iam", region_name=aws_region)
    role_details = iam_client.get_role(RoleName=role_name)
    role_arn = role_details["Role"]["Arn"]
    print(f"Role ARN fetched: {role_arn}")

    try:
        print("Creating Redshift Serverless Namespace...")
        redshift_client.create_namespace(
            namespaceName=namespace,
            adminUsername=admin_username,
            adminUserPassword=admin_password,
            dbName=database_name,
            iamRoles=[role_arn],
        )
        print(f"Namespace {namespace} created successfully")

        print("Creating Redshift Serverless Workgroup...")
        workgroup_response = redshift_client.create_workgroup(
            workgroupName=workgroup,
            namespaceName=namespace,
            baseCapacity=8,  # RCPU
            # TODO: Attach VPC or PrivateLink for production env
            publiclyAccessible=True,
        )
        print(f"Namespace {workgroup} created successfully")
        # Print the Redshift connection details
        workgroup_details = workgroup_response["workgroup"]
        print("Redshift Serverless is Ready!")
        print(f"JDBC URL: {workgroup_details['endpoint']['jdbcUrl']}")
        print(f"Database Name: {database_name}")
        print(f"Username: {admin_username}")
    except Exception as e:
        print(f"Error in Redshift setup {e}")


if __name__ == "__main__":
    setup_redshift()
