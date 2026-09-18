import time
import machine
import ubinascii
import dht

from machine import Pin, SoftSPI, SPI
from sx127x import SX127x


# ============================================================
# FIELDGUARD - SENDER
# Team Alpha | IoT Summer Camp Bremen 2026
# ============================================================


# ------------------------------------------------------------
# Device identification
# ------------------------------------------------------------

SENDER_ID = ubinascii.hexlify(
    machine.unique_id()
).decode().upper()

# Receiver used during the prototype.
# Replace this if your receiver prints a different hardware ID.
RECEIVER_ID = "YOUR_RECEIVER_ID"


# ------------------------------------------------------------
# Temperature thresholds
# ------------------------------------------------------------

WARNING_TEMP = 25
CRITICAL_TEMP = 30


# ------------------------------------------------------------
# DHT11 sensors
# ------------------------------------------------------------

sensor_z1 = dht.DHT11(Pin(16))
sensor_z2 = dht.DHT11(Pin(42))
sensor_z3 = dht.DHT11(Pin(41))

sensors = {
    "Z1": sensor_z1,
    "Z2": sensor_z2,
    "Z3": sensor_z3
}


# ------------------------------------------------------------
# LoRa configuration
# ------------------------------------------------------------

lora_parameters = {
    "frequency": 868000000,
    "frequency_offset": 0,
    "tx_power_level": 14,
    "signal_bandwidth": 125e3,
    "spreading_factor": 9,
    "coding_rate": 5,
    "preamble_length": 8,
    "implicitHeader": False,
    "sync_word": 0xF4,
    "enable_CRC": True,
    "invert_IQ": False,
    "debug": False,
}


lora_pins = {
    "dio_0": 46,
    "ss": 48,
    "reset": 45,
    "sck": 14,
    "miso": 21,
    "mosi": 47,
}


spi = SoftSPI(
    baudrate=10000000,
    polarity=0,
    phase=0,
    bits=8,
    firstbit=SPI.MSB,
    sck=Pin(lora_pins["sck"]),
    mosi=Pin(lora_pins["mosi"]),
    miso=Pin(lora_pins["miso"])
)


lora = SX127x(
    spi=spi,
    pins=lora_pins,
    parameters=lora_parameters
)


# ------------------------------------------------------------
# FieldGuard logic
# ------------------------------------------------------------

def get_status(temperature):

    if temperature is None:
        return "ERROR"

    if temperature >= CRITICAL_TEMP:
        return "CRITICAL"

    if temperature >= WARNING_TEMP:
        return "WARNING"

    return "NORMAL"


def read_sensor(zone, sensor):

    try:
        sensor.measure()

        temperature = sensor.temperature()
        humidity = sensor.humidity()

        status = get_status(temperature)

        return {
            "zone": zone,
            "temperature": temperature,
            "humidity": humidity,
            "status": status
        }

    except OSError as error:

        print(
            "{} sensor error: {}".format(
                zone,
                error
            )
        )

        return {
            "zone": zone,
            "temperature": None,
            "humidity": None,
            "status": "ERROR"
        }


def get_overall_status(readings):

    statuses = [
        reading["status"]
        for reading in readings
    ]

    if "CRITICAL" in statuses:
        return "CRITICAL"

    if "WARNING" in statuses:
        return "WARNING"

    if "ERROR" in statuses:
        return "ERROR"

    return "NORMAL"


def get_affected_zones(readings):

    affected = []

    for reading in readings:

        if reading["status"] != "NORMAL":
            affected.append(reading["zone"])

    if not affected:
        return "NONE"

    return ",".join(affected)


def format_value(value):

    if value is None:
        return "NA"

    return str(value)


def create_packet(counter, readings):

    overall = get_overall_status(readings)
    affected = get_affected_zones(readings)

    zone_parts = []

    for reading in readings:

        zone_parts.append(
            "{}:{},{},{}".format(
                reading["zone"],
                format_value(reading["temperature"]),
                format_value(reading["humidity"]),
                reading["status"]
            )
        )

    packet = "{}|{}|{}|{}|{}|{}|OVERALL:{}|AFFECTED:{}".format(
        RECEIVER_ID,
        SENDER_ID,
        counter,
        zone_parts[0],
        zone_parts[1],
        zone_parts[2],
        overall,
        affected
    )

    return packet


# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------

print()
print("======================================")
print(" FIELDGUARD - LoRa Sender")
print("======================================")
print("Sender ID   :", SENDER_ID)
print("Receiver ID :", RECEIVER_ID)
print("Frequency   : 868 MHz")
print("Sync word   : 0xF4")
print("======================================")
print()


counter = 0


while True:

    readings = []

    for zone, sensor in sensors.items():

        reading = read_sensor(
            zone,
            sensor
        )

        readings.append(reading)

        print(
            "{} | Temp: {} C | Humidity: {} % | {}".format(
                zone,
                format_value(reading["temperature"]),
                format_value(reading["humidity"]),
                reading["status"]
            )
        )

        # DHT11 needs a little time between measurements
        time.sleep(1)

    overall_status = get_overall_status(readings)
    affected_zones = get_affected_zones(readings)

    packet = create_packet(
        counter,
        readings
    )

    print()
    print("Overall :", overall_status)
    print("Affected:", affected_zones)
    print("Packet  :", packet)

    # Transmit over LoRa
    lora.println(packet)

    print("LoRa packet transmitted.")
    print("--------------------------------------")
    print()

    counter += 1

    time.sleep(5)
