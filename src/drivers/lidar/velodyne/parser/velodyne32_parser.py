    
    
from .velodyne_parser import VelodyneParser


class Velodyne32Parser(VelodyneParser):
    def generate_pointcloud(cls, scan_msg):
        cls.unpack(scan_msg)

    def unpack(cls, scan_msg):
        pass
