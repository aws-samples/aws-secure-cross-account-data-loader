# AWS Big Data Blog - Create an Amazon Redshift Data Warehouse That Can Be Securely Accessed Across Accounts

This code demonstrates the steps outlined on the AWS big data blog (https://aws.amazon.com/blogs/big-data/create-an-amazon-redshift-data-warehouse-that-can-be-securely-accessed-across-accounts/) on securely accessing and loading data across AWS accounts that was published on November 17, 2017.  It takes 
the Open FDA food enforcement dataset (https://open.fda.gov/downloads/) and performs slight transformations on the data before loading into a Redshift cluster located in a different account.


## Steps

1. Choose or create three different AWS accounts in which you are the owner 
	* We will refer to these accounts as "Source", "Loader" and "Target" respectively
2. Within the source and target accounts, create an IAM role which has an inline policy of the JSON contained in the "iam/cross_account_role_policy.json".
    * Also, add a trust policy to each of these roles that allows the Loader account to assume them.  An example can be viewed at "iam/cross_account_trust_policy.json".
3. Spin up a Redshift cluster in both the source and target accounts using the cloud_formation/redshift.yaml template
    * Attach a role to each of these clusters that has full access to S3
    * Make note of the endpoint of these clusters as you will need that info later
4. Spin up an EMR cluster in the Source account using the cloud_formation/emr_livy_loader.yaml template
    * SSH into the master node of the cluster and copy and run the emr_loader/emr_bootstrap_redshift_drivers.sh script	
	* This EMR cluster will need access to your source Redshift cluster so make sure the security group of the Redshift cluster allows this
5. Spin up a t2.micro EC2 instance in the source account and then copy over the emr_loader/driver.py and emr_loader/food_events.scala to the EC2
	* Run the driver.py file which will load the Open FDA food enforcement dataset into the source Redshift cluster using Apache livy
6. Replace the "<Your Target AWS Account ID>" with the AWS account ID of your target account in the cross_account_loader/resources/bucket_policy.json file
7. Replace the values in the cross_account_loader/resources/config.json with the appropriate values from the Source, Loader and Target accounts
8. Within the Loader account, create an S3 bucket and copy the files and directories contained within the "cross_account_loader" directory
    * Make sure that you do not copy the "cross_account_loader" directory itself
9. In the Loader account, run the CloudFormation template cloudformation/cross_account_loader.yaml specifying the S3 bucket from step 8 for the S3 bucket parameter
10. Connect to your target Redshift cluster and view that milk_food_enforcement table has been loaded with data.