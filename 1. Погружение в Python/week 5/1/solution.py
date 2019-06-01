import socket
import time 

class ClientError(socket.error):
	pass

class Client:
	def __init__(self, host, port, timeout=None):
		self.port = port
		self.host = host
		self.timeout = timeout
		self.connection = socket.create_connection((self.host, self.port), self.timeout)
		
	def _read(self):
		data = b''
		while not data.endswith(b'\n\n'):
			data += self.connection.recv(1024)

		status, new_data = data.decode().split('\n', 1)
		new_data = new_data.strip()
		if 'error' in status:
			raise ClientError()
		return new_data

	def put(self, key, value, timestamp=str(int(time.time()))):
		self.connection.sendall(f'put {key} {value} {timestamp}\n'.encode('utf8'))
		self._read()
			

	def get(self, key):
		self.connection.sendall(f'get {key}\n'.encode('utf8'))
		answer = self._read()
		if not answer:
			return {}

		data = {}
		for i in answer.split('\n'):
			server, metric_value, timestamp = i.split()
			if server not in data:
				data[server] = []
			data[server].append((int(timestamp), float(metric_value)))

		return data

# client = Client('127.0.0.1', 10001)
