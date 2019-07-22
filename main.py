from Walkline import Walkline, WalklineButton, WalklineSwitch
from WalklineUtility import WifiHandler
from utime import sleep
from config import *
from machine import Pin

led = Pin(2, Pin.OUT, value=0)


def main():
	Walkline.setup(UID, DEVICE_ID, DEVICE_KEY)

	button = WalklineButton(13, button_pressed)
	switch = WalklineSwitch(2, button_pressed)

	Walkline.run()


def connect_to_internet():
	result_code = WifiHandler.set_sta_mode(WIFI_SSID, WIFI_PASS)
	WifiHandler.set_ap_status(False)

	return result_code


def button_pressed(status=None):
	if status is None:
		led.value(not led.value())
	else:
		if status == 1:
			led.on()
		elif status == 0:
			led.off()
		elif status == 2:
			led.value(not led.value())
		else:
			raise ValueError("Wrong status command received")


if __name__ == "__main__":
	try:
		if WifiHandler.STATION_CONNECTED == connect_to_internet():
			while True:
				main()

				sleep(1)
	except KeyboardInterrupt:
		print("\nPRESS CTRL+D TO RESET DEVICE")
