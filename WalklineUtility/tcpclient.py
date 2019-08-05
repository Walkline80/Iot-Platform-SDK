from Walkline.WalklineConfig import *
from module import urequests
import ujson


class TCPClient(object):
	def __init__(self):
		self._response = None
		self._status_code = None
		self._reason = None
		self._text = None
		self._json = None

	def request(self, command: str, data: str):
		url = "{0}/{1}".format(WALKLINE_HTTP_SERVER, command)
		header = {'Content-Type': 'application/json'}
		# header = {"Content-Type": "application/x-www-form-urlencoded"}

		try:
			self._response = urequests.post(url, headers=header, data=data)
			self._status_code = self._response.status_code
			self._reason = str(self._response.reason, "utf-8")
			self._text = self._response.text
			self._json = self._response.json()
		except Exception as e:
			# [Errno 110] ETIMEDOUT
			print(e)

			with open(r"error.log", "a") as log:
				log.write(str(e) + "\r\n")
		finally:
			self._response.close()

	@property
	def status_code(self):
		return self._status_code

	@property
	def reason(self):
		return self._reason

	@property
	def text(self):
		return self._text

	def json(self):
		return self._json
