import struct
from datetime import datetime
import threading
import pathlib
import click
from serverclient.utils.listener import Listener


data_lock = threading.Lock()


class ClientHandler(threading.Thread):
    unpacker = struct.Struct('LLI')

    def __init__(self, conn, data_dir):
        super().__init__()
        self.conn = conn
        self.data_root = pathlib.Path(data_dir)

    def run(self):
        user_id, ts, thought = self.get_message()
        self.write_data(user_id, datetime.fromtimestamp(ts), thought)
        self.conn.close()

    def get_message(self):
        prefix_bytes_read = self.read_from_client(self.unpacker.size)
        user_id, ts, thought_size = self.unpacker.unpack(prefix_bytes_read)
        thought = self.read_from_client(thought_size)
        return user_id, ts, thought.decode(encoding='utf-8')

    def read_from_client(self, expected_size):
        return self.conn.receive(expected_size)

    def write_data(self, user_id, date_time, thought):
        data_dir_path = self.data_root / str(user_id)
        data_file_path = data_dir_path / date_time.strftime(
            '%Y-%m-%d_%H-%M-%S.txt')
        data_lock.acquire()
        try:
            data_dir_path.mkdir(parents=True, exist_ok=True)
            if data_file_path.exists():
                with data_file_path.open('a') as data_file:
                    data_file.write(f'\n{thought}')
            else:
                with data_file_path.open('w') as data_file:
                    data_file.write(f'{thought}')
        finally:
            data_lock.release()


@click.command()
@click.option('--host', '-h', help='A host for the server to run on')
@click.option('--port', '-p', help='A port for the server to run on')
@click.option('--data', '-d', help='Data directory for server to store in')
def run_server(host, port, data):
    listener = Listener(int(port), host)
    listener.start()
    while True:
        conn = listener.accept()
        client_handler = ClientHandler(conn, data)
        client_handler.start()


if __name__ == '__main__':
    run_server()
