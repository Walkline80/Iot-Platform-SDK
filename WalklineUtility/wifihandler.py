import network

_station_status_message = {
	network.STAT_IDLE: "network idle",
	# network.STAT_CONNECT_FAIL: "network connect failed",
	network.STAT_CONNECTING: "",
	network.STAT_GOT_IP: "Connected",
	network.STAT_NO_AP_FOUND: "could not found ap",
	network.STAT_WRONG_PASSWORD: "wrong password given"
}


class WifiHandler:
	AP_MODE = 0
	STA_MODE = 1
	STATION_CONNECTED = network.STAT_GOT_IP

	def __init__(self):
		pass

	@staticmethod
	def set_ap_status(active: bool):
		access_point = network.WLAN(network.AP_IF)
		access_point.active(active)

	@staticmethod
	def set_sta_status(active: bool):
		station = network.WLAN(network.STA_IF)
		station.active(active)

	@staticmethod
	def set_sta_mode(essid, password):
		from utime import sleep_ms

		station = network.WLAN(network.STA_IF)

		station.active(False)
		station.active(True)

		print("\nConnecting to network...")

		if not station.isconnected():
			station.connect(essid, password)

			while not station.isconnected():
				result_code = station.status()

				# result_code == network.STAT_CONNECT_FAIL or\
				if result_code == network.STAT_IDLE or\
					result_code == network.STAT_GOT_IP or\
					result_code == network.STAT_NO_AP_FOUND or\
					result_code == network.STAT_WRONG_PASSWORD:
					break
				elif result_code == network.STAT_CONNECTING:
					pass

				sleep_ms(500)

		status_code = station.status()

		print(_station_status_message[status_code])
		print(station.ifconfig())

		return status_code

	@staticmethod
	def gateway():
		import network

		gateway = None
		station = network.WLAN(network.STA_IF)

		if station.status() == network.STAT_GOT_IP:
			gateway = station.ifconfig()[2]

		return gateway
