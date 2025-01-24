from collections import deque
from dataclasses import dataclass, field
from struct import unpack

from drivers.lidar.velodyne.constant.velodyne_packet import *
from src.common.util.message_util import Header
from src.drivers.lidar.velodyne.proto.config import Mode


@dataclass
class RawLaser:
    packet: bytes
    distance: float = 0
    reflectivity: int = 0

    def __post_init__(self):
        pass


@dataclass
class RawBlock:
    block_packet: bytes
    block_id: int = 0  # UPPER_BANK or LOWER_BANK
    rotation: int = 0  # 0-35999, divide by 100 to get degrees
    firing_raw_packet: bytes = b''
    
    def __post_init__(self):
        self.rotation = unpack(AZIMUTH_PACKET_FORMAT,self.block_packet[FLAG_PACKET_SIZE:FLAG_PACKET_SIZE+AZIMUTH_PACKET_SIZE])[0]
        self.firing_raw_packet = self.block_packet[HEADER_PACKET_SIZE:BLOCK_SIZE]


@dataclass
class RawPacket:
    raw_packet: bytes
    block: list[RawBlock] = []
    gps_timestamp: float = 0
    status_type: int = 0
    status_value: int = 0



@dataclass
class NMEATime:
    year: int = 0
    mon: int = 0
    day: int = 0
    hour: int = 0
    min: int = 0
    sec: int = 0


@dataclass
class VelodynePacket:
    stamp: float = 0  # nano sec
    data: bytes = b''
    

@dataclass
class VelodyneInfo(Header):
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
class VelodyneScan(Header):
    model: str = ''
    mode: Mode = Mode.STRONGEST
    firing_packets: deque[VelodynePacket] = field(default_factory=deque([]))
    positioning_packets: bytes = b''
    velodyne_info: VelodyneInfo = field(default_factory=VelodyneInfo())
    basetime: float = 0  # nano sec