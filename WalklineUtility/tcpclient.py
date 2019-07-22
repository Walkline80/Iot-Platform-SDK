from Walkline.WalklineConfig import *
import urequests
import ujson


class TCPClient(object):
	def __init__(self):
		self._response = None

	def request(self, command: str, data: str):
		url = "http://{0}:{1}/{2}".format(WALKLINE_HTTP_SERVER, WALKLINE_HTTP_PORT, command)
		header = {'Content-Type': 'application/json'}

		print("url:", url)
		print("data:", ujson.dumps(data))

		self._response = urequests.post(url, headers=header, data=ujson.dumps(data))

	def status_code(self):
		return self._response.status_code

	def reason(self):
		return str(self._response.reason, "utf-8")

	def text(self):
		return self._response.text

	def json(self):
		return self._response.json()
