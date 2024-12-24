from dataclasses import dataclass


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
    
