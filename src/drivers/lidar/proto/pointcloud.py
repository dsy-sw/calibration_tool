from dataclasses import dataclass, field

from common.proto.message import Header


@dataclass
class PointXYZIT:
    x: float = 0
    y: float = 0
    z: float = 0
    intensity: int = 0
    timetamp: float = 0
    

@dataclass
class PointCloud(Header):
    point: list[PointXYZIT] = field(default_factory=[])
    measurement_time: float = 0