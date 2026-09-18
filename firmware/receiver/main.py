import time
import machine
import ubinascii

from machine import Pin, SoftSPI, SPI
from sx127x import SX127x


# ============================================================
# FIELDGUARD - RECEIVER
# Team Alpha | IoT Summer Camp Bremen 2026
# ============================================================


# ------------------------------------------------------------
# Receiver hardware ID
# ------------------------------------------------------------

RECEIVER_ID = ubinascii.hexlify(
    machine.unique_id()
).decode().upper()


# ------------------------------------------------------------
# Alert hardware
# ------------------------------------------------------------

BUZZER_PIN = 39
LED_PIN = 40

buzzer = Pin(
    BUZZER_PIN,
    Pin.OUT
)

led = Pin(
    LED_PIN,
    Pin.OUT
)

buzzer.off()
led.off()


# ------------------------------------------------------------
# LoRa configuration
# MUST match sender
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
# Packet processing
# ------------------------------------------------------------

def parse_zone(zone_string):

    zone_name, data = zone_string.split(
        ":",
        1
    )

    values = data.split(",")

    if len(values) != 3:
        raise ValueError(
            "Invalid zone data"
        )

    temperature = values[0]
    humidity = values[1]
    status = values[2]

    return {
        "zone": zone_name,
        "temperature": temperature,
        "humidity": humidity,
        "status": status
    }


def parse_packet(payload):

    parts = payload.split("|")

    if len(parts) != 8:
        raise ValueError(
            "Invalid FieldGuard packet"
        )

    destination_id = parts[0]
    sender_id = parts[1]
    counter = parts[2]

    z1 = parse_zone(parts[3])
    z2 = parse_zone(parts[4])
    z3 = parse_zone(parts[5])

    overall = parts[6].replace(
        "OVERALL:",
        ""
    )

    affected = parts[7].replace(
        "AFFECTED:",
        ""
    )

    return {
        "destination": destination_id,
        "sender": sender_id,
        "counter": counter,
        "zones": [
            z1,
            z2,
            z3
        ],
        "overall": overall,
        "affected": affected
    }


# ------------------------------------------------------------
# Alert behaviour
# ------------------------------------------------------------

def normal_alert():

    led.off()
    buzzer.off()


def warning_alert():

    led.on()

    # Short warning beep
    buzzer.on()
    time.sleep(0.15)
    buzzer.off()


def critical_alert():

    led.on()

    # Three urgent pulses
    for _ in range(3):

        buzzer.on()
        time.sleep(0.20)

        buzzer.off()
        time.sleep(0.15)


def error_alert():

    # Two short pulses for sensor/packet error
    for _ in range(2):

        led.on()
        time.sleep(0.10)

        led.off()
        time.sleep(0.10)


def apply_alert(status):

    if status == "CRITICAL":
        critical_alert()

    elif status == "WARNING":
        warning_alert()

    elif status == "ERROR":
        error_alert()

    else:
        normal_alert()


# ------------------------------------------------------------
# Display packet in serial console
# ------------------------------------------------------------

def display_packet(data, rssi):

    print()
    print("======================================")
    print(" FIELDGUARD - RECEIVED DATA")
    print("======================================")

    print(
        "Sender  :",
        data["sender"]
    )

    print(
        "Packet  :",
        data["counter"]
    )

    print(
        "RSSI    :",
        rssi,
        "dBm"
    )

    print("--------------------------------------")

    for zone in data["zones"]:

        print(
            "{} | Temp: {} C | Humidity: {} % | {}".format(
                zone["zone"],
                zone["temperature"],
                zone["humidity"],
                zone["status"]
            )
        )

    print("--------------------------------------")

    print(
        "Overall :",
        data["overall"]
    )

    print(
        "Affected:",
        data["affected"]
    )

    print("======================================")
    print()


# ------------------------------------------------------------
# Main receiver loop
# ------------------------------------------------------------

print()
print("======================================")
print(" FIELDGUARD - LoRa Receiver")
print("======================================")
print("Receiver ID :", RECEIVER_ID)
print("Frequency   : 868 MHz")
print("Sync word   : 0xF4")
print("Waiting for FieldGuard packets...")
print("======================================")
print()


while True:

    if lora.receivedPacket():

        try:

            payload = lora.readPayload()

            # Some SX127x versions return bytes,
            # others return a string.
            if isinstance(
                payload,
                bytes
            ):
                payload = payload.decode(
                    "utf-8"
                )

            payload = payload.strip()

            rssi = lora.packetRssi()

            data = parse_packet(
                payload
            )

            # ------------------------------------------------
            # Destination filtering
            # ------------------------------------------------

            if data["destination"] != RECEIVER_ID:

                print(
                    "Packet ignored. Destination:",
                    data["destination"]
                )

                continue

            display_packet(
                data,
                rssi
            )

            apply_alert(
                data["overall"]
            )

        except Exception as error:

            print(
                "Receiver error:",
                error
            )

    time.sleep(0.05)
