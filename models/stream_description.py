import datetime
from models.shard import Shard
from typing import List, Optional

class StreamDescription:
    """
    Represents a description of a stream.

    Attributes:
        stream_name (str): The name of the stream.
        stream_arn (str): The Amazon Resource Name (ARN) of the stream.
        stream_status (str): The current status of the stream.
        stream_mode (str): The mode of the stream (e.g., 'ON_DEMAND' or 'PROVISIONED').
        shards (List[Shard]): A list of shards in the stream.
        has_more_shards (bool): Indicates if there are more shards available.
        retention_period_hours (int): The retention period of the stream in hours.
        stream_creation_timestamp (Optional[int]): The timestamp when the stream was created.
        encryption_type (str): The type of encryption used for the stream.
        key_id (Optional[str]): The ID of the encryption key.
    """
    def __init__(self, stream_name: str, stream_arn: str, stream_status: str, stream_mode: str, shards: List[Shard], has_more_shards,
        retention_period_hours: int, stream_creation_timestamp, encryption_type: str, key_id: str) -> None:
        self.stream_name = stream_name
        self.stream_arn = stream_arn
        self.stream_status = stream_status
        self.stream_details = {
            'StreamMode': stream_mode
        }
        self.shards = shards
        self.has_more_shards = has_more_shards
        self.retention_period_hours = retention_period_hours
        self.stream_creation_timestamp = stream_creation_timestamp
        self.encryption_type = encryption_type
        self.key_id = key_id

    @classmethod
    def from_dict(cls, data_dict):
        """
            Transform the coming dict to a instance of StreamDescription

            Attributes:
                cls (StreamDescription): The class to transform to (StreamDescription)
                data_dict (str): The data of the dict to use to transform to StreamDescription
        """
        timestamp = data_dict["StreamCreationTimestamp"]
        if isinstance(timestamp, str):
            timestamp = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))


        return cls(
            stream_name=data_dict["StreamName"],
            stream_arn=data_dict["StreamARN"],
            stream_status=data_dict["StreamStatus"],
            stream_mode=data_dict["StreamModeDetails"]["StreamMode"],
            shards= [Shard.from_dict(shard) for shard in data_dict["Shards"]],
            has_more_shards=data_dict["HasMoreShards"],
            retention_period_hours=data_dict["RetentionPeriodHours"],
            stream_creation_timestamp = timestamp,
            encryption_type=data_dict["EncryptionType"],
            key_id=data_dict["KeyId"]
        )

    def __repr__(self) -> str:
        return f"StreamDescription(stream_name={self.stream_name}, stream_arn={self.stream_arn}, shards={self.shards})"
