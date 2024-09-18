import time

from services.thread import mqtt_thread

ob_mqtt_thread = mqtt_thread.MqttThread("localhost", 1883, "device/voltage", "world")
ob_mqtt_thread.start()

while True:
    time.sleep(1)
    if ob_mqtt_thread.is_alive():
        continue
    ob_mqtt_thread.start()
