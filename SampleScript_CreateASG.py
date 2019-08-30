import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    client = boto3.client('cloudformation')
    pipeline = boto3.client('codepipeline')
    
    UserParam=event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
    UserParams = json.loads(UserParam)
    AMINameType = UserParams["AMINameType"]
    StackName = UserParams["StackName"]
    ProjectName = UserParams["ProjectName"]
    InstanceType= UserParams["InstanceType"]
    MaxPrice= UserParams["MaxPrice"]
    MinInstanceNumber= UserParams["MinInstanceNumber"]
    MaxInstanceNumber= UserParams["MaxInstanceNumber"]
    PemKeyName= UserParams["PemKeyName"]
    SecurityGroupId= UserParams["SecurityGroupId"]
    SubnetId= UserParams["SubnetId"]
    
    #getting the new golden AMI
    AMI_ID_Details = ec2.describe_images(Filters=[{'Name': 'tag:Version', 'Values': ['Latest'] },{'Name': 'tag:Name','Values': [AMINameType]}])
    NewGoldenAMI=AMI_ID_Details['Images'][0]['ImageId']
    print(NewGoldenAMI)
    
    #getting current launch configuration name
    stackDetails = client.describe_stacks(StackName=StackName)
    LaunchConfigName = stackDetails['Stacks'][0]['Parameters']
    tagvalue = ''             
    for i in LaunchConfigName: 
        if i['ParameterKey'] == 'LaunchConfigurationName':
            tagvalue = i["ParameterValue"]
    
    #creating new launch config name  
    LaunchConfig=(str(tagvalue.split("-")[0]))
    old_version_number=(float(tagvalue.split("-")[1]))
    new_version_number=str(old_version_number + 1)   
    NewLaunchConfigName=LaunchConfig+'-'+new_version_number
    
    print (stackDetails)
    print (LaunchConfigName)
    print(tagvalue)
    print (LaunchConfig)
    print(NewLaunchConfigName)
    

    #updating the cloud formation stack with new AMI 
    response = client.update_stack(
    StackName=StackName,
    UsePreviousTemplate=True,
    Parameters=[
        {
            'ParameterKey': 'ImageName',
            'ParameterValue': NewGoldenAMI,
        },
        {
            'ParameterKey': 'AutoScalingGroupName',
            'UsePreviousValue': True,
        },
        {
            'ParameterKey': 'LaunchConfigurationName',
            'ParameterValue': NewLaunchConfigName,
        },
        {
            'ParameterKey': 'InstanceType',
            'ParameterValue': InstanceType,
        },
        {
            'ParameterKey': 'MaxInstanceNumber',
            'ParameterValue': MaxInstanceNumber,
        },
        {
            'ParameterKey': 'MaxPrice',
            'ParameterValue': MaxPrice,
        },
        {
            'ParameterKey': 'MinInstanceNumber',
            'ParameterValue': MinInstanceNumber,
        },
        {
            'ParameterKey': 'PemKeyName',
            'ParameterValue': PemKeyName,
        },
        {
            'ParameterKey': 'SecurityGroupId',
            'ParameterValue': SecurityGroupId,
        },
        {
            'ParameterKey': 'SubnetId',
            'ParameterValue': SubnetId,
        },
    ],
    Tags=[
        {
            'Key': 'Project',
            'Value': ProjectName
        },
    ],
)
    pipelineResponse = pipeline.put_job_success_result(jobId=event['CodePipeline.job']['id'])
    return pipelineResponse