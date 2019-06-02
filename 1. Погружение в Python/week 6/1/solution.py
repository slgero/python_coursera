import asyncio

class Storage:
	def __init__(self):
		self.storage = {}

	def put(self, data):
		try:
			cmd, data = data.split(' ', 1)
			data = data.strip()
			key, value, timestamp = data.split()
			if key not in self.storage:
				self.storage[key] = {}
			self.storage[key][int(timestamp)] = float(value)
		except ValueError:
			raise RuntimeError

	def get_all(self):
		to_send = 'ok\n'
		for key, value in self.storage.items():
			for time, val in sorted(value.items()):
				to_send += f'{key} {str(val)} {str(time)}\n'
		to_send += '\n'
		return to_send

	def get(self, data, transport):
		cmd, data = data.split(' ', 1)
		data = data.strip()
		if data == '*':
			return self.get_all()

		if data not in self.storage:
			return "ok\n\n"

		to_send = 'ok\n'
		for time, val in sorted(self.storage[data].items()):
			to_send += f'{data} {str(val)} {str(time)}\n'
		to_send += '\n'

		return to_send


class Parser:
	def what_is_it(self, data):
		try:
			cmd, value = data.split(' ', 1)
			if cmd == 'put': return 'put'
			elif cmd == 'get': return 'get'
			else:
				raise RuntimeError
		except:
			raise RuntimeError


class ClientServerProtocol(asyncio.Protocol):
	storage = Storage()

	def __init__(self):
		super().__init__()
		self.parser = Parser()
		self.buff = b''

	def connection_made(self, transport):
		self.transport = transport

	def data_received(self, data):
		self.buff += data
		try:
			buff_decode = self.buff.decode()
		except UnicodeDecodeError:
			print('Что-то не так с расшифровкой данных')
			return

		if not buff_decode.endswith('\n'):
			return

		self.process_data(buff_decode)
		self.buff = b''

	def process_data(self, data):
		try:
			ans = self.parser.what_is_it(data)
			if ans == 'put':
				self.storage.put(data)
				self.transport.write('ok\n\n'.encode())
			else:
				self.transport.write(self.storage.get(data, self.transport).encode())
		except RuntimeError:
			self.transport.write('error\nwrong command\n\n'.encode())
			return


def run_server(host, port):
	loop = asyncio.get_event_loop()
	coro = loop.create_server(
	    ClientServerProtocol,
	    host, port
	)

	server = loop.run_until_complete(coro)

	try:
	    loop.run_forever()
	except KeyboardInterrupt:
	    pass

	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()


# run_server('127.0.0.1', 8888)
