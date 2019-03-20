import json
import requests
from bs4 import BeautifulSoup
import logging
import boto3
import csv
import re

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
    content=event["Records"][0]["Sns"]["Message"]
    #print(event["Records"][0]["Sns"]["Message"])
    lst=(re.split("[[]|{|,|[]]|:|}",content))
    #print(lst)
    cont=[each for each in lst if each != '']
    key=cont[-1]
    keywords = cont[0:len(cont)-1]
    #print(keywords,key)
    s3client=boto3.client('s3',aws_access_key_id="",
         aws_secret_access_key= "")
    result=scrape(keywords)
    print(result)
    with open("/tmp/keywords.csv","w") as f:
        w=csv.DictWriter(f,result[0].keys())
        w.writeheader()
        w.writerows(result)
    s3client.upload_file('/tmp/keywords.csv','demodownloadslambda',key+".csv")

#main({'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-2:726784664986:Keywords:33dfe598-bec4-49a3-8511-36c9f7a89811', 'Sns': {'Type': 'Notification', 'MessageId': '28c0f4e6-b352-5a55-9c21-a1ecb86e2d4f', 'TopicArn': 'arn:aws:sns:us-east-2:726784664986:Keywords', 'Subject': None, 'Message': 'Apple, Nike, Dheeraz', 'Timestamp': '2019-03-18T21:09:16.488Z', 'SignatureVersion': '1', 'Signature': 'PoUiWTsvyEXVbdN2oJ4G5P/s+HRHlwSdJ16XO8ZtW7NP1xRjjKDW/0kPkvmP6QDQMUfdW625WDTVOU6+9tKBkA3P5RywKbTeELeRgLeIeZlq/cUnkwsqy/TDCG4mg3a3WjmWubEusQyhiVNnhtsdudROn8ObIQO3Asg6o2ONbi/VUXrCm1iO3Sfnk9Tr9c4LYIdohfQZzZLIPyJpGqIGSAVJgMumKGuMcADTaPws6ynOHdnfF31P2i+AkhdbyCHsLOeXd3ShUIJHcv5Ak/xSlIzEvFfxNhneCOvK/uBs+T6eOQobnNcw15QpND0nGtSzq/VFGGTJX9Sf2tqVxOID+Q==', 'SigningCertUrl': 'https://sns.us-east-2.amazonaws.com/SimpleNotificationService-6aad65c2f9911b05cd53efda11f913f9.pem', 'UnsubscribeUrl': 'https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:726784664986:Keywords:33dfe598-bec4-49a3-8511-36c9f7a89811', 'MessageAttributes': {}}}]},"")

