from collections import deque
from dataclasses import dataclass, field


@dataclass
class VelodynePacket:
    stamp: float = 0  # nano sec
    data: bytes = b''


@dataclass
class NMEATime:
    year: int = 0
    mon: int = 0
    day: int = 0
    hour: int = 0
    min: int = 0
    sec: int = 0
    

@dataclass
class VelodyneInfo:
    timestamp: float = 0
    top_temperature: int = 0
    bottom_temperature: int = 0
    currente_temperature: int = 0
    temperature_after_ADC: int = 0
    timestamp_after_ADC: int = 0
    reason_of_ADC: int = 0
    state_of_ADC: int = 0
    top_of_the_microsec: int = 0
    pulse_per_sec: int = 0
    state_of_temperature: int = 0
    latest_temperature: int = 0
    AC_temperature: int = 0


@dataclass
class VelodyneScan:
    timestamp: float = 0  # sec
    model: str = ''
    firing_packets: deque[VelodynePacket] = field(default_factory=deque([]))
    positioning_packets: bytes = b''
    velodyne_info: VelodyneInfo = field(default_factory=VelodyneInfo())
    basetime: float = 0  # nano sec