from dataclasses import dataclass, field


@dataclass
class PointXYZIT:
    x: float
    y: float
    z: float
    intensity: int
    timestamp: int  # nano sec


@dataclass
class Point3D:
    x: float
    y: float
    z: float


@dataclass
class Point2D:
    x: float
    y: float


@dataclass
class Quaternion:
    qx: float
    qy: float
    qz: float
    qw: float
    

@dataclass
class PointLLH:
    lat: float
    lon: float
    height: float


@dataclass
class Polygon2D:
    points: list[tuple[float,float]] = field(default_factory=[])


@dataclass
class Polygon3D:
    points: list[(float,float,float)] = field(default_factory=[])