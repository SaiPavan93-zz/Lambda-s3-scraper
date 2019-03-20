import boto3
import json

sns=boto3.client('sns',region_name='us-east-2',aws_access_key_id="",
         aws_secret_access_key= "ß")

response = sns.publish(
    TopicArn='arn:aws:sns:us-east-2:726784664986:Keywords',
    Message="Welcome to Springbuk!!"


)

print(response)

#"default":"{\"keywords\":[\"apple\",\"Sony\"],\"key\":\"lad\"}"