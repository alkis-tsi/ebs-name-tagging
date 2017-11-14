### Author Alkiviadis Tsitsigkos
### Augusy 2016, London UK
import boto3
import dpath
import json

def lambda_handler(event, context):
    json_event = json.dumps(event)
    readable_json = json.loads(json_event)
    instance_id = ''
    if event['detail-type'] == 'AWS API Call via CloudTrail' and event['detail']['eventName'] == 'RunInstances':
        for (path,value)in dpath.util.search(readable_json, '**/instanceId', yielded=True):
            instance_id = value
    name_tag = nametag(instance_id)
    volume_id = getvolumeid(instance_id)
    create_nametag = createnametag(volume_id, name_tag)


def nametag(instance_id):
    client = boto3.client('ec2','eu-west-1')
    response1 = client.describe_tags(
        Filters=[
                    {
                        'Name':'resource-id',
                        'Values':[instance_id],
                    }
                ]
            )
    tags = response1['Tags']
    name_tag = ''
    for tag in tags
        if tag['Key'] == 'Name':
            name_tag = tag['Value']
            break
    return name_tag

def get_volume_id(instance_id):
    client = boto3.client('ec2','eu-west-1')
    response2 = client.describe_instances(
        InstanceIds=[instance_id],
        Filters=[
                {
                    'Name':'block-device-mapping.volume-id',
                    'Values':['*']
                }
            ]
        )

    for (path,value) in dpath.util.search(response2,'**/VolumeId', yielded=True):
        volume_id = value
    return volume_id

def create_name_tag(volume_id,name_tag):
    client = boto3.client('ec2','eu-west-1')
    response3 = client.create_tags(
        Resources=[volume_id],
            Tags=[
                    {
                        'Key':'Name',
                        'Value':name_tag
                    }
                ]
        )
