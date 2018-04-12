import re
import boto3
import json
from boto3.dynamodb.conditions import Key
client = boto3.client('cognito-idp')
def lambda_handler(event, context):
    print(event)
    cogres = client.list_users(
    UserPoolId='us-east-1_NdStkSybm',
    AttributesToGet=[
        'email',
    ],
    
)
    #print(event['Username'])
    d1 = cogres['Users']
    for i in reversed(range(len(d1))):
        temp = d1[i]['Attributes'][0]['Value']
        if re.match('.+@gmail\.com$', temp):
            client.admin_delete_user(
                UserPoolId='us-east-1_NdStkSybm',
                Username=d1[i]['Username']
            )
            return { "statusCode" : 302, "headers": { "Location" : "https://s3.amazonaws.com/amogh-s-baalti/redirect.html" }}
            
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BidderReg')
    dbres = table.scan()
    items = dbres['Items']
    print(cogres)
    r = len(d1)
    for i in reversed(range(r)):
        temp = d1[i]['Attributes'][0]['Value']
        print(items)
        if re.match('([a-z]+\.[a-z]+){1}@quantiphi\.com$', temp):
            if items==[]:
                table.put_item(Item={'EmailID': temp,'Amt':1000})
                return { "statusCode" : 302, "headers": { "Location" : "https://b60bj5zuv3.execute-api.us-east-1.amazonaws.com/LATEST/SchedulePage?eid="+temp+"&amt=1000" }}
            elif temp not in items[0]['EmailID']:
                table.put_item(Item={'EmailID': temp,'Amt':1000})
                return { "statusCode" : 302, "headers": { "Location" : "https://b60bj5zuv3.execute-api.us-east-1.amazonaws.com/LATEST/SchedulePage?eid="+temp+"&amt=1000" }}
            else:
                schRes= table.query(KeyConditionExpression=Key('EmailID').eq(items[0]['EmailID']))
                print(schRes)
                amt = str(schRes['Items'][0]['Amt'])
                return { "statusCode" : 302, "headers": { "Location" : "https://b60bj5zuv3.execute-api.us-east-1.amazonaws.com/LATEST/SchedulePage?eid="+items[0]['EmailID']+"&amt="+amt }}