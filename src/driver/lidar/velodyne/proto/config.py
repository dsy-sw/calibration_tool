from dataclasses import dataclass, field

from driver.lidar.velodyne.constant.device import DeviceModel, Mode


@dataclass
class VelodyneConfig:
    frame_id: str
    firing_data_port: int  # 데이터 수신
    positioning_data_port: int  # 데이터 송신
    model: DeviceModel
    rpm: int = 600
    mode: Mode = field(default_factory=Mode.STRONGEST)
    is_main_frame: bool = False