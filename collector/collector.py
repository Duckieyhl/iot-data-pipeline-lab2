import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Cấu hình InfluxDB
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "9QEHrxYzIRG19OYY2zBGbTmoECERDf11HOTKvglBzvZzpeKq1ZD2R6ghgwvk6MNpS4eYpdY2pFOUvxW99CBjDQ=="
INFLUX_ORG = "1 minh tao"
INFLUX_BUCKET = "iot_telemetry"

client_db = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_db.write_api(write_options=SYNCHRONOUS)

MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "ptit/iot/sensors"

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("Received payload:", data)
        
        # Tạo point ghi dữ liệu Time-Series
        point = Point("sensor_data") \
            .tag("device_id", "esp32_wokwi") \
            .field("temperature", float(data["temperature"])) \
            .field("humidity", float(data["humidity"])) \
            .field("distance_cm", float(data["distance_cm"])) \
            .field("rssi", int(data["rssi"]))
        
        write_api.write(bucket=INFLUX_BUCKET, record=point)
        print("-> Saved to InfluxDB")
    except Exception as e:
        print("Error processing message:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_forever()
