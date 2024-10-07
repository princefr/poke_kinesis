import boto3
import base64
import math
from collections import Counter
import gzip
import json



# Initialize clients for Kinesis and KMS
kinesis_client = boto3.client('kinesis', region_name='eu-west-1')
kms_client = boto3.client('kms', region_name='eu-west-1')

def read_and_decrypt_kinesis_data(shard_iterator):
    # Get records from Kinesis
    response = kinesis_client.get_records(
        ShardIterator=shard_iterator,  # You will need to get this from `get_shard_iterator()`
        Limit=10  # Adjust the limit based on your needs
    )

    records = response['Records']

    # Process each record
    for record in records:
        encrypted_data = record['Data']
        decrypted_response = gzip.decompress(encrypted_data)
        print(decrypted_response)

# Example usage
stream_name = 'siri-destineo-et-sbx'


shard_response = kinesis_client.describe_stream(StreamName=stream_name)
shard_id = shard_response['StreamDescription']['Shards'][1]['ShardId']
shard_iterator_response = kinesis_client.get_shard_iterator(
    StreamName=stream_name,
    ShardId=shard_id,
    ShardIteratorType='TRIM_HORIZON'  # You can also use 'TRIM_HORIZON' or other iterator types
)

shard_iterator = shard_iterator_response['ShardIterator']


read_and_decrypt_kinesis_data(shard_iterator)