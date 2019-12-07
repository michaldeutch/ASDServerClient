from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.listening_socket = socket.socket()

    def __repr__(self):
        return f'Listener(port={self.port!r}, host={self.host!r}, backlog' \
               f'={self.backlog!r}, reuseaddr={self.reuseaddr!r})'

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        if self.reuseaddr:
            self.listening_socket.setsockopt(socket.SOL_SOCKET,
                                             socket.SO_REUSEADDR, 1)
        self.listening_socket.bind((self.host, self.port))
        self.listening_socket.listen(self.backlog)

    def stop(self):
        self.listening_socket.close()

    def accept(self):
        conn, _ = self.listening_socket.accept()
        return Connection(conn)
