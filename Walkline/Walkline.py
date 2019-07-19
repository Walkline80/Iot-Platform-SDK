import _thread
from micropython import const
from machine import Pin
from utime import ticks_ms, sleep_ms
from WalklineUtility.tcpclient import *
from Walkline import WalklineConfig


class Protocol(object):
	def __init__(self):
		self.thread = None
		self.is_thread_running = False
		self.uid = None
		self.device_id = None
		self.device_key = None
		# self.buttons = {}
		self.switches = {}
		self.client = TCPClient()


Protocol = Protocol()


class WalklineMPY(object):
	@staticmethod
	def setup(uid, device_id, device_key):
		Protocol.uid = uid
		Protocol.device_id = device_id
		Protocol.device_key = device_key

	def run(self):
		if not Protocol.is_thread_running:
			Protocol.thread = _thread.start_new_thread(self._thread_run, ())
			Protocol.is_thread_running = True

	def _thread_run(self):
		while True:
			self.check_data()

	def check_data(self):
		Protocol.client.request(DeviceCommand.QUERY_COMMAND, self._collect_status())

	@staticmethod
	def _collect_status():
		result = '{'

		for switch in Protocol.switches:
			result += '"type":"switch","status":"{0:d}",'.format(switch.status())

		return eval(result + '}')


Walkline = WalklineMPY()


class WalklineButton(object):
	_BUTTON_RESPONSE_INTERVAL = const(100)

	def __init__(self, pin: int, callback: callable):
		self._button = Pin(pin, Pin.OPEN_DRAIN, Pin.PULL_UP)
		self._callback = callback
		self._last_ticks = ticks_ms()
		self._count = 0

		self._button.irq(self._button_response_cb, Pin.IRQ_FALLING)

		# Protocol.buttons["button"] = self

	def _button_response_cb(self, button):
		if ticks_ms() - self._last_ticks > self._BUTTON_RESPONSE_INTERVAL:
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
