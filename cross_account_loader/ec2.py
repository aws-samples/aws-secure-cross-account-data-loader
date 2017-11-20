import boto3

def add_ingress_rule(role_arn='<your role arn>', cidr_ip='0.0.0.0/32', role_session_name='CrossAccountSecurityGroupIngress', security_group_id='<your security group>', ip_protocol='tcp', region='us-west-2', from_port=5439, to_port=5439):
    client = boto3.client('sts')
    sts_response = client.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name)
    ec2 = boto3.client('ec2', region_name=region, aws_session_token=sts_response['Credentials']['SessionToken'], aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],  aws_access_key_id=sts_response['Credentials']['AccessKeyId'])
    ec2.authorize_security_group_ingress(CidrIp=cidr_ip,FromPort=from_port,ToPort=to_port,GroupId=security_group_id, IpProtocol=ip_protocol)


def revoke_ingress_rule(role_arn='<your role arn>', cidr_ip='0.0.0.0/32', role_session_name='CrossAccountSecurityGroupIngress', security_group_id='<your security group>', ip_protocol='tcp', region='us-west-2', from_port=5439, to_port=5439):
    client = boto3.client('sts')
    sts_response = client.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name)
    ec2 = boto3.client('ec2', region_name=region, aws_session_token=sts_response['Credentials']['SessionToken'], aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],  aws_access_key_id=sts_response['Credentials']['AccessKeyId'])
    ec2.revoke_security_group_ingress(CidrIp=cidr_ip,FromPort=from_port,ToPort=to_port,GroupId=security_group_id, IpProtocol=ip_protocol)


