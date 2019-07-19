from Walkline import Walkline, WalklineButton
from WalklineUtility import WifiHandler
from utime import sleep
from .config import *
from machine import Pin

led = Pin(2, Pin.OUT, value=1)


def main():
	Walkline.setup(UID, DEVICE_ID, DEVICE_KEY)
	Walkline.run()


def connect_to_internet():
	result_code = WifiHandler.set_sta_mode(WIFI_SSID, WIFI_PASS)
	WifiHandler.set_ap_status(False)

	return result_code


def button_pressed(status=None):
	if status is None:
		led.value(not led.value())
	else:
		if isinstance(status, str):
			if status == "on":
				led.on()
			elif status == "off":
				led.off()
			elif status == "toggle":
				led.value(not led.value())
			else:
				raise ValueError("Wrong status command received")
		else:
			raise TypeError("Status is not string")


if __name__ == "__main__":
	try:
		button = WalklineButton(5, button_pressed)

		if WifiHandler.STATION_CONNECTED == connect_to_internet():
			while True:
				main()

				sleep(0.1)
	except KeyboardInterrupt:
		print("\nPRESS CTRL+D TO RESET DEVICE")
