import boto3

def put_bucket_policy(role_arn, bucket, bucket_policy, role_session_name='CrossAccountCreateBucketPolicy', region='us-west-2'):
    client = boto3.client('sts')
    sts_response = client.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name)
    s3 = boto3.client('s3', region_name=region, aws_session_token=sts_response['Credentials']['SessionToken'], aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],  aws_access_key_id=sts_response['Credentials']['AccessKeyId'])
    s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)


def delete_bucket_policy(role_arn, bucket, role_session_name='CrossAccountDeleteBucketPolicy', region='us-west-2'):
    client = boto3.client('sts')
    sts_response = client.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name)
    s3 = boto3.client('s3', region_name=region, aws_session_token=sts_response['Credentials']['SessionToken'],
                      aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                      aws_access_key_id=sts_response['Credentials']['AccessKeyId'])
    s3.delete_bucket_policy(Bucket=bucket)



