import threading
import asyncio
from typing import List
from bleak import BleakScanner
from edge.conf import BT_Loc

class BleScanner(threading.Thread):
    def __init__(self, result_queue:List):
        super().__init__()
        self.daemon = True
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.scanner = BleakScanner()
        self.scanner.register_detection_callback(self.detection_callback)
        self.result_queue = result_queue

    def detection_callback(self, device, advertisement_data):
        # Put the detected device address and RSSI into the queue
        if (BT_Loc.UUID in device.address):
            self.result_queue.put((device.address, device.rssi, advertisement_data.local_name))

    def run(self):
        self.loop.run_until_complete(self.start_scanning())

    async def start_scanning(self):
        await self.scanner.start()
        print("Started scanning...")
        try:
            while True:
                await asyncio.sleep(.01)
        except asyncio.CancelledError:
            await self.scanner.stop()