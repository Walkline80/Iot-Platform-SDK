import _thread
from micropython import const
from machine import Pin, WDT
from utime import ticks_ms, sleep_ms, sleep
from WalklineUtility.tcpclient import *
from Walkline import WalklineConfig
import gc


class Protocol(object):
	def __init__(self):
		self.thread = None
		self.is_thread_running = False
		self.uuid = None
		self.device_id = None
		self.device_key = None
		# self.buttons = {}
		self.switches = {}
		self.client = TCPClient()


Protocol = Protocol()


class WalklineMPY(object):
	def __init__(self):
		self._wdt = None

	@staticmethod
	def setup(uuid, device_id, device_key):
		Protocol.uuid = uuid
		Protocol.device_id = device_id
		Protocol.device_key = device_key

	def run(self):
		if not Protocol.is_thread_running:
			Protocol.thread = _thread.start_new_thread(self._thread_run, ())
			Protocol.is_thread_running = True

	def _thread_run(self):
		self._wdt = WDT(timeout=10000)
		self._wdt.feed()

		while True:
			self.check_data()

			sleep(2)

	def check_data(self):
		self._wdt.feed()
		self._wdt.feed()

		Protocol.client.request(DeviceCommand.QUERY_COMMAND, ujson.dumps(self._collect_status()))
		print(Protocol.client.text)

		# try:
		json = Protocol.client.json()

		if json['wanted_status'] != -1:
			Protocol.switches[Protocol.device_id].set_status(json['wanted_status'])
		# except Exception:
		# 	pass

		gc.collect()

	@staticmethod
	def _collect_status():
		result = '{'

		result += '"uuid":"{0}", "device_id":"{1}", "device_key":"{2}", '\
			.format(Protocol.uuid, Protocol.device_id, Protocol.device_key)

		for index, switch in Protocol.switches.items():
			result += '"type":"switch","status":{0:d},'.format(switch.status())

		return eval(result + '}')


Walkline = WalklineMPY()

_BUTTON_RESPONSE_INTERVAL = const(100)


class WalklineButton(object):
	def __init__(self, pin: int, callback: callable):
		self._button = Pin(pin, Pin.IN, Pin.PULL_UP)
		self._callback = callback
		self._last_ticks = ticks_ms()
		self._count = 0

		self._button.irq(self._button_response_cb, Pin.IRQ_FALLING)

		# Protocol.buttons["button"] = self

	def _button_response_cb(self, button):
		if ticks_ms() - self._last_ticks > _BUTTON_RESPONSE_INTERVAL:
			if button.value() == 0:
				self._callback()
				self._count += 1

				sleep_ms(50)

		self._last_ticks = ticks_ms()

	def count(self):
		return self._count


class WalklineSwitch(object):
	def __init__(self, pin: int, callback: callable):
		self._switch = Pin(pin, Pin.OUT)
		self._callback = callback

		Protocol.switches[Protocol.device_id] = self

	def status(self):
		return self._switch.value()

	def set_status(self, status):
		self._callback(status)
