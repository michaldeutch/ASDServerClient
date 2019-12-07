import socket


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        _, my_port = self.socket.getsockname()
        _, other_port = self.socket.getpeername()
        return f'<Connection from 127.0.0.1:{my_port} to 127.0.0.1' \
            f':{other_port}>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        chunks = []
        bytes_read = 0
        while bytes_read < size:
            chunk = self.socket.recv(min(size - bytes_read, size))
            if not chunk:
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_read = bytes_read + len(chunk)
        return b''.join(chunks)

    def close(self):
        self.socket.close()
