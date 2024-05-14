# IR head +++++++++++++++++++
serial_port = "/dev/ttyUSB0"

# MQTT +++++++++++++++++++
mqtt = "127.0.0.1:1883"          # e.g. "192.168.0.123:1883"; set None to disable MQTT
mqtt_user = None                 # "<user>:<pwd>"
mqtt_topic = "eBZaehler"         # "eBZaehler"

# csv settings +++++++++++++++++++
write_csv = True
buffer_to_write = 1800           # preserve SD card ;-)
csv_path = "/home/pi/Public/"

# too much ketchup +++++++++++++++++++
cycle = 1                        # messages/seconds to publish/log

