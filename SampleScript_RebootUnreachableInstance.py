import boto3
import pprint

def lambda_handler(event, context):
	
	filters = [
	            {
	                'Name': 'tag:Owner',
	                'Values': ['Gokul']
	            },
	            {
                    'Name': 'instance-state-name', 
                    'Values': ['running']
                }
	           ]


	client = boto3.client('ec2')

	
	i = 0
	Runinstances = []
	response =  client.describe_instances(Filters=filters)
	
	for i in response['Reservations']:
	    Runinstances.append(i['Instances'][0]['InstanceId'])
	
	i = 0    
	for i in Runinstances:
		response1 = client.describe_instance_status(InstanceIds=[i])
		if response1['InstanceStatuses'][0]['SystemStatus']['Status'] and response1['InstanceStatuses'][0]['InstanceStatus']['Status'] == 'ok':
			pprint.pprint(i + " is Good")
		else:
			pprint.pprint(i + " is being restarted")