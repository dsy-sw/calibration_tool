from dataclasses import dataclass, field
from math import ceil

from driver.lidar.velodyne.constant.device import PACKET_RATE, DeviceModel, Mode


@dataclass
class VelodyneConfig:
    frame_id: str
    firing_data_port: int  # 데이터 수신
    positioning_data_port: int  # 데이터 송신
    model: DeviceModel
    rpm: int = 600  # 300~1200
    mode: Mode = field(default_factory=Mode.STRONGEST)
    is_main_frame: bool = False
    npacket: float = 0
    
    def __post_init__(self):
        if not self.model.name in PACKET_RATE.keys():
            raise KeyError(f"{self.model.name} is not exist.")
        self.npacket = ceil(PACKET_RATE[self.model.name] / (self.rpm / 60.0))