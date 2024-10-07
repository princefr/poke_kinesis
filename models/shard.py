from typing import List, Optional


class Shard:
    """
    Represents a description of a shard

    Attribute:
        shard_id (str): The identification number of the shard.
        starting_hash_key (str): The sarting hashing key.
        ending_hash_key (str): The ending hashing key.
        starting_sequence_number (str): The starting sequence number

    """
    def __init__(self, shard_id: str, starting_hash_key: str, ending_hash_key: str, starting_sequence_number: str) -> None:
        self.shard_id = shard_id
        self.hash_key_range =  {
            'StartingHashKey': starting_hash_key,
            'EndingHashKey': ending_hash_key,
        }
        self.sequence_number_range = {
            'StartingSequenceNumber': starting_sequence_number,
        }


    @classmethod
    def from_dict(cls, data_dict):
        """
            Transform the coming dict to a instance of Shard

            Attributes:
                cls (Shard): The class to transform to (Shard)
                data_dict (str): The data of the dict to use to transform to Shard
        """
        return cls(
            shard_id=data_dict['ShardId'],
            starting_hash_key=data_dict['HashKeyRange']['StartingHashKey'],
            ending_hash_key=data_dict['HashKeyRange']['EndingHashKey'],
            starting_sequence_number=data_dict['SequenceNumberRange']['StartingSequenceNumber']
        )

    def __repr__(self):
            return (f"Shard(shard_id={self.shard_id}, "
                    f"hash_key_range={self.hash_key_range}, "
                    f"sequence_number_range={self.sequence_number_range})")
