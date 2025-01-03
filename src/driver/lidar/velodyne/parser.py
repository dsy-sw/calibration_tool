

from driver.lidar.velodyne.constant.device import BLOCKS_PER_PACKET


class VelodyneParser:
    def __init__(self):
        pass
    

class Velodyne16Parser:
    def generate_pointcloud(cls, scan_msg):
        cls.unpack(scan_msg)
        
    def unpack(cls, scan_msg):
        pass
    
    
class Velodyne32Parser:
    def generate_pointcloud(cls, scan_msg):
        cls.unpack(scan_msg)

    def unpack(cls, scan_msg):
        pass