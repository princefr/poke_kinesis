import datetime
import gzip
import json
from typing import List, Optional


class KinesisRecord:
    """
    Represents a description of a Kinesis record

    Attributes:
        sequence_number: The sequence number.
        approximate_arrival_timestamp:  The approximate arrival time as a timestamp.
        data:  The gzip reprensentation of the data.
        partition_key: The partition key of the record.
        encryption_type: The encryption type of the record (Default = KMS).
    """
    def __init__(self, sequence_number, approximate_arrival_timestamp, data, partition_key, encryption_type: str) -> None:
        self.sequence_number = sequence_number
        self.approximate_arrival_timestamp = approximate_arrival_timestamp
        self.data = data
        self.parition_key = partition_key
        self.encryption_type = encryption_type

    @classmethod
    def from_dict(cls, data_dict):
        """
            Transform the coming dict to a instance of KinesisRecord

            Attributes:
                cls (KinesisRecord): The class to transform to (KinesisRecord)
                data_dict (str): The data of the dict to use to transform to KinesisRecord
        """
        timestamp = data_dict['ApproximateArrivalTimestamp']
        if isinstance(timestamp, str):
            timestamp = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

        return cls(
            sequence_number=data_dict['SequenceNumber'],
            approximate_arrival_timestamp=data_dict['ApproximateArrivalTimestamp'],
            data=data_dict['Data'],
            partition_key=data_dict['PartitionKey'],
            encryption_type=data_dict['EncryptionType']
        )

    def decode_data(self):
        """Decode the base64 encoded data"""
        try:
            decrypted_data = gzip.decompress(self.data)
            return decrypted_data

        except Exception as e:
            print(f'Error decoding data: {e}')
            return None

    def __repr__(self) -> str:
        return f"KinesisRecord(sequence_number={self.sequence_number}, timestamp={self.approximate_arrival_timestamp})"

    @staticmethod
    def parse_records(records_string) :
        try:
            if isinstance(records_string, str):
                records_data = json.loads(records_string)
            elif isinstance(records_string, list):
                records_data = records_string
            else:
                raise ValueError(f"Expected string or list, got {type(records_string)}")
            return [KinesisRecord.from_dict(record) for record in records_data]
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return[]

        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
