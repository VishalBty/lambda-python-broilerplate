
import boto3
import os
import json
import uuid

MAX_DELAY_SECONDS = 60 * 2

sqs_client = boto3.client("sqs", region_name="us-east-1")


def verbose(*args, **kwargs):
    """
    Prints the arguments passed to it if the environment variable USER is set to "mypc"
    :param args: arguments to be printed
    :param kwargs: keyword arguments to be printed
    """
    if os.environ.get("USER") == "mypc":
        print(*args, **kwargs)

def send_sqs_message(body: dict, queue_url: str, delay: int = 0):
    """
    Sends a single message to an SQS queue
    :param body: message body
    :param queue_url: URL of the SQS queue
    :param delay: delay in seconds before the message is available for processing
    """
    _ = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(body),
        DelaySeconds=delay,
    )


def send_sqs_messages(queue_url: str, messages: list, delay: int, is_fifo: bool = False):
    """
    Sends multiple messages to an SQS queue
    :param queue_url: URL of the SQS queue
    :param messages: list of messages to be sent
    :param delay: delay in seconds before the messages are available for processing
    :param is_fifo: whether the queue is a FIFO queue or not
    """
    delay = MAX_DELAY_SECONDS if delay > MAX_DELAY_SECONDS else delay
    index = 0

    while index < len(messages):
        batch_messages = messages[index:index + 10]
        index += 10

        entries = []
        for _message in batch_messages:

            _entry = {
                'Id': str(uuid.uuid4()),
                'MessageBody': json.dumps(_message, default=str),
                'DelaySeconds': delay
            }
            if is_fifo:
                _entry['MessageGroupId'] = _message.get(
                    'MessageGroupId', str(uuid.uuid4()))
                _entry['MessageDeduplicationId'] = _message.get(
                    'MessageDeduplicationId', str(uuid.uuid4()))
                del _entry['DelaySeconds']
            entries.append(_entry)
        verbose(f"Sending {entries} to {queue_url}")
        _ = sqs_client.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries,
        )


def yield_rows(cursor, chunk_size):
    """
    Generator to yield chunks from cursor
    :param cursor: database cursor
    :param chunk_size: size of each chunk
    :return: generator object that yields chunks
    """
    chunk = []
    for i, row in enumerate(cursor):
        if i % chunk_size == 0 and i > 0:
            yield chunk
            del chunk[:]
        chunk.append(row)
    yield chunk


def cursor_to_sqs(cursor, queue_url, delay_steps=0.1, chunk_size=100, is_fifo=False):
    """
    Sends the results of a database query to an SQS queue
    :param cursor: database cursor
    :param queue_url: URL of the SQS queue
    :param delay_steps: delay in seconds between each chunk of messages
    :param chunk_size: size of each chunk
    :param is_fifo: whether the queue is a FIFO queue or not
    """
    if cursor:

        if hasattr(cursor, "batch_size"):
            cursor.batch_size(chunk_size)

        chunks = yield_rows(cursor=cursor,
                            chunk_size=chunk_size)
        _delay = 0
        count = 0
        for chunk in chunks:
            _delay += delay_steps
            count += len(chunk)
            send_sqs_messages(queue_url=queue_url,
                              messages=chunk, delay=int(round(_delay)), is_fifo=is_fifo)

        verbose(f"Records found: {count}")
