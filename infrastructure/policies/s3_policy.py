{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:ListBucket", "s3:GetObject", "s3:PutObject"],
            "Resource": [
                "arn:aws:s3:::brain-tumor-bucket-5af1ff41-b833-4ce2-9443-b48296bbe849",
                "arn:aws:s3:::brain-tumor-bucket-5af1ff41-b833-4ce2-9443-b48296bbe849/*",
            ],
        },
        {
            "Effect": "Allow",
            "Action": [
                "redshift-serverless:CreateNamespace",
                "redshift-serverless:GetNamespace",
                "redshift-serverless:ListNamespaces",
                "redshift-serverless:CreateWorkgroup",
                "redshift-serverless:GetWorkgroup",
                "redshift-serverless:ListWorkgroups",
            ],
            "Resource": ["*"],
        },
    ],
}
