from dataclasses import dataclass, field


@dataclass
class PointXYZIT:
    x: float = 0
    y: float = 0
    z: float = 0
    intensity: int = 0
    timetamp: float = 0
    

@dataclass
class PointCloud:
    frame_id: str = ''
    point: list[PointXYZIT] = field(default_factory=[])
    measurement_time: float = 0