import json
import time
import logging
import os

from guest import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(event['body'])
    if 'guests' not in data or 'rsvp' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the guest item.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # update the todo in the database
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#rsvp': 'rsvp',
        },
        ExpressionAttributeValues={
          ':rsvp': True,
          ':total_of_guests': len(data['guests']),
          ':confirmed_guests': data['guests']),
          ':rsvpedAt': timestamp,
        },
        UpdateExpression='SET #rsvp = :rsvp, '
                         'total_of_guests = :total_of_guests, '
                         'confirmed_guests = :confirmed_guests',
                         'rsvpedAt = :rsvpedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
