import json
from abc import ABC, abstractmethod
from tqdm import tqdm

class Signal(ABC):
    signal_name = None

    def __init__(self, timestamp, raw_data):
        self.timestamp = timestamp
        self.raw_data = raw_data
        self.parsed_data = self.parse(raw_data)

    @abstractmethod
    def parse(self, raw):
        ...

    def __repr__(self):
        return f"{self.__class__.__name__}(timestamp={self.timestamp}, parsed_data={self.parsed_data})"

class ImuSignal(Signal):
    signal_name = "ImuData"

    def parse(self, raw):
        # TODO: convert raw values to physical units
        return None


class OdometryVelocitySignal(Signal):
# "payload": [
#     {
#         "type":0,
#         "timestamp":1977130951,
#         "value":3.65625,
#         "variance":0.0006698595825582743,
#         "confidence":0
#     },
#     {
#         "type":1,
#         "timestamp":1977130951,
#         "value":0.0,
#         "variance":0.0,
#         "confidence":0
#     }
# ]
    signal_name = "OdometryVelocities"

    def parse(self, raw):
        # TODO: convert raw values to physical units
        return None


class OdometryAngularRateSignal(Signal):
    signal_name = "OdometryAngularRates"

    def parse(self, raw):
        # TODO: convert raw values to physical units
        return None

class GnssPositionSignal(Signal):
    signal_name = "GnssPositions"

    def parse(self, raw):
        # TODO: convert raw values to physical units
        return None

SIGNAL_CLASSES = {
    "ImuData": ImuSignal,
    "OdometryVelocities": OdometryVelocitySignal,
    "OdometryAngularRates": OdometryAngularRateSignal,
    "GnssPositions": GnssPositionSignal,
}

SIGNALS = []

with open("dumps/masters_dump_1.json") as f:
    data = json.load(f)

    for item in tqdm(data, desc="Parsing signals from dump file"):
        signal_class = SIGNAL_CLASSES.get(item["signal_name"])

        if signal_class is None:
            continue

        signal_class.raw_data = item["payload"]
        signal_class.timestamp = item["timestamp"]
        signal_class.parse(signal_class, item["payload"])


