from datetime import datetime
import struct


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'{self.__class__.__name__}(user_id={self.user_id!r},  ' \
               f'timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        return f'[{self.timestamp}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        return isinstance(other, Thought) and self.__dict__ == other.__dict__

    def serialize(self):
        print(f'packing {self.user_id}, '
              f' {int(datetime.timestamp(self.timestamp))},'
              f' {len(self.thought)}, {self.thought}')
        return struct.pack('LLI', self.user_id,  int(datetime.timestamp(
            self.timestamp)), len(self.thought)) + bytes(self.thought, 'utf-8')

    @staticmethod
    def deserialize(data):
        bytes_format = struct.Struct('LLI')
        user_id, ts, thought_size = bytes_format.unpack(data[
                                                        :bytes_format.size])
        timestamp = datetime.fromtimestamp(ts)
        thought_bytes = data[bytes_format.size:bytes_format.size+thought_size]
        thought = thought_bytes.decode(encoding='utf-8')
        return Thought(user_id, timestamp, thought)
