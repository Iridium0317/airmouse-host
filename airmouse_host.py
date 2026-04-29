import asyncio
import struct
from bleak import BleakClient, BleakScanner
from pynput.mouse import Controller

NUS_TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
DEVICE_NAME = "AirMouse"

mouse = Controller()
packet_count = 0

def on_packet(_, data: bytearray):
    global packet_count
    packet_count += 1
    if len(data) != 4:
        print(f"  bad len {len(data)}: {data.hex()}")
        return
    dx, dy = struct.unpack("<hh", data)
    if packet_count % 20 == 0:
        print(f"  pkt#{packet_count}  dx={dx:+5d}  dy={dy:+5d}")
    if dx or dy:
        mouse.move(dx, dy)

async def main():
    print(f"Scanning for {DEVICE_NAME}...")
    device = await BleakScanner.find_device_by_name(DEVICE_NAME, timeout=15.0)
    if not device:
        print("Not found")
        return
    print(f"Found {device.address}, connecting...")

    async with BleakClient(device) as client:
        print("Connected. Subscribing to TX...")
        await client.start_notify(NUS_TX_UUID, on_packet)
        print("Streaming. Ctrl-C to stop.")
        while client.is_connected:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
