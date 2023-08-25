import json
from config import get_mongodb_client
from helper import *
from something_doer import SomethingDoer

def handle_body(database, body):
    """
    Handles the body of the event and performs some operation using SomethingDoer.

    Args:
    - database: A MongoDB database object.
    - body: A JSON string representing the body of the event.

    Returns:
    - None
    """
    record_body = json.loads(body)
    doer = SomethingDoer(database)
    doer.do_it()
    print("done")

def lambda_handler(event, context):
    """
    The entry point for the AWS Lambda function.

    Args:
    - event: A dictionary containing the event data.
    - context: An object containing the runtime information.

    Returns:
    - A dictionary containing the HTTP status code and an empty body.
    """
    client = get_mongodb_client()
    database = client.something

    if 'Records' in event:
        records = event['Records']
        for record in records:
            handle_body(database, record['body'])

    elif 'body' in event:
        handle_body(database, event['body'])

    return {
        'statusCode': 200,
        'body': ''
    }
