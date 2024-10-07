from typing import Tuple
import boto3
from botocore import serialize
from botocore.exceptions import ClientError
from botocore.useragent import Optional
from boto3.dynamodb.types import TypeDeserializer
from models.kinesis_records import KinesisRecord
import os
from models.stream_description import StreamDescription

os.environ['AWS_PROFILE'] = ""
STREAM_NAME=""
REGION_NAME=""




class Kinesis:
    """
        Represents a Kinesis instance object


        Attributes:
            stream_name (str): The name of the stream.
            region_name (str): The region name to start the AWS Kinesis instance

    """
    def __init__(self, stream_name: str, region_name:str) -> None:
        self.stream_name = stream_name
        self.region_name = region_name
        self.kinesis_client = boto3.client('kinesis', region_name=region_name)
        self.kms = boto3.client('kms', region_name=region_name)


    def decrypt(self, encrypted):
            response = self.kms.decrypt(CiphertextBlob=encrypted)
            print(response)

    def describe_stream(self) -> Optional[str]:
        """Describes the Kinesis stream"""
        try:
            response = self.kinesis_client.describe_stream(StreamName=self.stream_name)
            return response['StreamDescription']

        except Exception as e:
            print(f"Error describin the stream: {e}")
            return None

    def get_shard_iterator(self, shard_id: str, iterator_type: str = "TRIM_HORIZON") -> Optional[str]:
        """Gets a shard iterator"""
        print(shard_id)
        try:
            response= self.kinesis_client.get_shard_iterator(
                StreamName=self.stream_name,
                ShardId=shard_id,
                ShardIteratorType=iterator_type
            )
            return response['ShardIterator']

        except Exception as e:
            print(f"Error getting shard iterator: {e}")
            return None

    def get_records(self, shard_iterator: str, limit: int = 10) -> Tuple[Optional[str], Optional[str]]:
        """Reads records from the Kinesis stream"""

        try:
            response = self.kinesis_client.get_records(ShardIterator=shard_iterator, Limit=limit)
            return response['Records'], response['NextShardIterator']
        except Exception as e:
            print(f"Error getting records: {e}")
            return None, None


if __name__=="__main__":
    kinesis = Kinesis(stream_name=STREAM_NAME, region_name=REGION_NAME)
    response = kinesis.describe_stream()
    print(response)
    if response:
        stream_description = StreamDescription.from_dict(response)
        for shard in stream_description.shards:
            shard_iterator = kinesis.get_shard_iterator(shard.shard_id)
            if shard_iterator:
                records, s = kinesis.get_records(shard_iterator)
                kinesis_records = KinesisRecord.parse_records(records_string=records)
                for record in kinesis_records:
                    print(record)
