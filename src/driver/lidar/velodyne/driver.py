from driver.lidar.velodyne.proto.config import VelodyneConfig
from sub_modules.bridge.socket.socket import get_socket


class VelodyneDriver:
    def __init__(self, config: VelodyneConfig):
        frequency = (config.rpm() / 60.0)

    def set_basetime_from_nmeatime(self):
        pass
    
    def set_basetime(self):
        pass

    def poll_positioning_packet(self):
        pass

    def poll_standard(self):
        pass

    def update_gps_to_hour(self):
        pass
