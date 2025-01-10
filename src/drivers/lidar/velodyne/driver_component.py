

from threading import Thread

from drivers.lidar.velodyne.driver.velodyne_driver import VelodyneDriverFactory
from drivers.lidar.velodyne.proto.config import VelodyneConfig
from drivers.lidar.velodyne.proto.data_proto import VelodyneScan


class VelodyneDriverComponent:
    def __init__(self, config: VelodyneConfig):
        
        self.driver = VelodyneDriverFactory.create_driver(config)
        self.device_thread = Thread(target=self.device_poll, args=(config,))
        self.device_thread.start()

    def device_poll(self, config: VelodyneConfig):
        driver = self.driver
        while 1: # while 조건에 system 상태 추가 예정
            scan_data = VelodyneScan()
            if driver.Poll(scan_data):
                pass