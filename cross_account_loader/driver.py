import ec2, redshift, json, s3
from urllib2 import urlopen

config = json.load(open('resources/config.json'))
public_ip = urlopen("http://169.254.169.254/latest/meta-data/public-ipv4").read()


#unload from source cluster
def unload():
    ec2.add_ingress_rule(role_arn=config['source_sg_role_arn'], security_group_id=config['source_security_group_id'], cidr_ip= public_ip + '/32')
    source_connection = redshift.connect("dbname ='dev' user = " + config['source_db_username'] + " host =" + config['source_db_host'] + \
                                  " password =" + config['source_db_password'] + " port='5439'")
    redshift.unload(source_connection, redshift_role=config['source_redshift_role_arn'], s3bucket=config['s3bucket'], s3key=config['s3key'], sql_transform=open('resources/unload_transform.sql').read())
    ec2.revoke_ingress_rule(role_arn=config['source_sg_role_arn'], security_group_id=config['source_security_group_id'], cidr_ip= public_ip + '/32')


#load into target cluster
def copy():
    ec2.add_ingress_rule(role_arn=config['target_sg_role_arn'], security_group_id=config['target_security_group_id'], cidr_ip= public_ip + '/32')
    target_connection = redshift.connect("dbname ='dev' user = " + config['target_db_username'] + " host =" + config['target_db_host'] + \
                                  " password =" + config['target_db_password'] + " port='5439'")
    redshift.execute_ddl(con=target_connection, ddl=open('resources/target_ddl.sql').read())
    redshift.copy(target_connection, redshift_role=config['target_redshift_role_arn'], s3bucket=config['s3bucket'], s3key=config['s3key'], table='milk_food_enforcement')
    ec2.revoke_ingress_rule(role_arn=config['target_sg_role_arn'], security_group_id=config['target_security_group_id'], cidr_ip= public_ip + '/32')


def add_bucket_policy():
    bucket_policy = json.load(open('resources/bucket_policy.json'))
    bucket_policy = json.dumps(bucket_policy)
    s3.put_bucket_policy(role_arn=config['source_sg_role_arn'], bucket=config['s3bucket'], bucket_policy=bucket_policy)


def remove_bucket_policy():
    s3.delete_bucket_policy(role_arn=config['source_sg_role_arn'], bucket=config['s3bucket'])


def execute():
    unload()
    add_bucket_policy()
    copy()
    remove_bucket_policy()


if __name__ == "__main__":
    execute()

