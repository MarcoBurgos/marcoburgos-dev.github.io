import json
import logging
import os


import boto3
dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'id' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the guest item.")


    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': data['id']),
        'name': data['name']),
        'no_of_guests': data['no_of_guests']),
        'total_of_guests': None,
        'guests': data['guests'],
        'confirmed_guests': None,
        'rsvp': False,
        'phone': data['phone'],
        'rsvpedAt': None,
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
