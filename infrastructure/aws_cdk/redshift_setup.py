import os
import boto3
from setup_s3_iam_role import role_arn

aws_region = "us-east-1"

# Initialize Serverless Redshift Instance
workgroup = "batch_processing_project_workgroup"
namespace = "batch_processing_project_namespace"
database_name = "dev_db"
admin_username = "admin"
admin_passowrd = os.environ["ADMIN_PASSWORD"]
redshift_client = boto3.client("redshift-serverless", region_name=aws_region)

print("Creating Redshift Serverless Namespace...")
namespace_response = redshift_client.create_namespace(
    namespaceName=namespace,
    adminUsername=admin_username,
    adminUsernamePassword=admin_passowrd,
    dbName=database_name,
    iamRoles=[role_arn],
)
print(f"Namespace {namespace} created successfully")

print("Creating Redshift Serverless Workgroup...")
workgroup_response = redshift_client.create_workgroup(
    workgroupName=workgroup,
    namespaceName=namespace,
    baseCapacity=8,  # RCPU
    # TODO: for more secure action, setup VPC or PrivateLink
    publiclyAccessible=True,
)
print(f"Namespace {workgroup} created successfully")
# Print the Redshift connection details
workgroup_details = workgroup_response["workgroup"]
print("\n🚀 Redshift Serverless is Ready! 🚀")
print(f"JDBC URL: {workgroup_details['endpoint']['jdbcUrl']}")
print(f"Database Name: {database_name}")
print(f"Username: {admin_username}")
