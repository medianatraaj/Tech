import json
import boto3
import datetime
import dateutil
from datetime import datetime, timedelta
from datetime import date
from dateutil import parser

client = boto3.client('ecs')
client1 = boto3.client('ec2')

def lambda_handler(event, context):
    date_object2 = datetime.utcnow()
    date_object3 = datetime.strftime(date_object2,"%Y-%m-%d")
    dt1 = dateutil.parser.parse(date_object3).date()
    response = client.list_clusters()
    for i in response['clusterArns']:
        response1 = client.list_container_instances(cluster = i)
        for j in response1['containerInstanceArns']:
            response2 = client.describe_container_instances(cluster=i,containerInstances=[j])
            k = response2['containerInstances'][0]['registeredAt']
            oldIns = response2['containerInstances'][0]['ec2InstanceId']
            date_object1 = datetime.strftime(k,"%Y-%m-%d")
            dt2 = dateutil.parser.parse(date_object1).date()
            date_diff = dt1 - dt2
            if (date_diff.days > 7):
                print(oldIns)
#               client1.terminate_instances(InstanceIds=[k])