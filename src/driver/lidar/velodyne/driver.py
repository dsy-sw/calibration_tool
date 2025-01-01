from time import time

from driver.lidar.velodyne.proto.config import VelodyneConfig
from sub_modules.bridge.socket.socket import SOCKET_KIND, get_socket


class VelodyneDriver:
    def __init__(self, config: VelodyneConfig):
        self.input_sock = get_socket(SOCKET_KIND.UDP,'input_sock',time(),'',config.firing_data_port,'localhost',0,receive_callback=None,buffer=1024*8)
        self.positioning_sock = get_socket(SOCKET_KIND.UDP,'input_sock',time(),'',config.positioning_data_port,'localhost',0,receive_callback=None,buffer=1024*8)


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


class VelodyneDriverFactory:
    def create_driver(config: VelodyneConfig):
        driver = VelodyneDriver(config)

        return driver