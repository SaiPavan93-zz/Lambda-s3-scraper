import json
import requests
from bs4 import BeautifulSoup
import logging
import boto3
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig()

def scrape(keywords):
    response = []
    for each in keywords:
        r = requests.get("https://www.google.com/search?q=" + each)
        logging.info("Google was successfully connected")

        bs = BeautifulSoup(r.text, features="html.parser")
        for link in bs.find_all('div', {'class': 'g'}):
            title = link.find('a')
            url = link.find('cite')
            if title and url:
                response.append({'keyword':each, 'title': title.text, 'url': url.text})
                #logging.info("Added title: %s, and URL: %s", title.text, url.text)
    return(response)
def main(event,context):
    #logging.info(event)
    key=event["Records"][0]["s3"]["object"]["key"]
    bucket=event["Records"][0]["s3"]["bucket"]["name"]
    s3client=boto3.client('s3',aws_access_key_id="AKIAIFRF5AC5Y6F2NU5A",
         aws_secret_access_key= "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")
    s3 = boto3.resource('s3', aws_access_key_id="AKIAIFRF5AC5Y6F2NU5A",
                        aws_secret_access_key="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")
    s3.Object(bucket,key).download_file("/tmp/keywords.txt")
    with open("/tmp/keywords.txt",'rb') as f:
        text=f.read().decode('utf-8')
        lines=(text.split("\n"))
    result=scrape(lines)
    logging.info(result[0].keys())
    with open("/tmp/keywords.csv","w") as f:
        w=csv.DictWriter(f,result[0].keys())
        w.writeheader()
        w.writerows(result)
    s3client.upload_file('/tmp/keywords.csv','demodownloadslambda',key+".csv")



#main({'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-2', 'eventTime': '2019-03-17T16:55:12.245Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'A2J2XPWWOKLGG6'}, 'requestParameters': {'sourceIPAddress': '50.90.245.227'}, 'responseElements': {'x-amz-request-id': '25A403F5EBB5B73F', 'x-amz-id-2': 'xAas0SIbOhrMdLI6exAdjI6PP5rTnLvaHIUn836XpwRnMUmTrA8P5PXkzbErbi8AwaeY75n9UN4='}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'f11593bd-0ad4-48ab-ab7c-6fc3346bbcda', 'bucket': {'name': 'democslambda', 'ownerIdentity': {'principalId': 'A2J2XPWWOKLGG6'}, 'arn': 'arn:aws:s3:::democslambda'}, 'object': {'key': 'keywords.txt', 'size': 20, 'eTag': 'fc651344089e57a0e96b7ed9662ce33a', 'sequencer': '005C8E7BF036720E81'}}}]},"")

