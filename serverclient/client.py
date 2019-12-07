import socket
import struct
import calendar
import time
from .utils import Connection


packer = struct.Struct('LLI')


def create_message_prefix_by_format(user_id, thought):
    ts = calendar.timegm(time.gmtime())
    return packer.pack(user_id, ts, len(thought)) + thought.encode()


def upload_thought(address, user, thought):
    sock = socket.socket()
    host, port = address
    sock.connect((host, port))
    conn = Connection(sock)
    formatted_message = create_message_prefix_by_format(int(user), thought)
    conn.send(formatted_message)
    conn.close()
    print('done')


if __name__ == '__main__':
    upload_thought()
