import os
import boto3
from dotenv import load_dotenv
from setup_s3_iam_role import setup_s3_iam_role

load_dotenv()

role_arn = setup_s3_iam_role()


def setup_redshift():
    aws_region = "us-east-1"
    # Initialize Serverless Redshift Instance
    workgroup = "brain_tumor_workgroup"
    namespace = "brain_tumor_namespace"
    database_name = "dev_db"
    admin_username = "admin"
    admin_password = os.getenv("ADMIN_PASSWORD")
    redshift_client = boto3.client("redshift-serverless", region_name=aws_region)

    try:
        print("Creating Redshift Serverless Namespace...")
        namespace_response = redshift_client.create_namespace(
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
        print("\n🚀 Redshift Serverless is Ready! 🚀")
        print(f"JDBC URL: {workgroup_details['endpoint']['jdbcUrl']}")
        print(f"Database Name: {database_name}")
        print(f"Username: {admin_username}")
    except Exception as e:
        print(f"Error in Redshift setup {e}")


if __name__ == "__main__":
    setup_redshift()
