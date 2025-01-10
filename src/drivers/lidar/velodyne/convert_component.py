import logging

from drivers.lidar.velodyne.constant.device import BLOCKS_PER_PACKET
from drivers.lidar.velodyne.parser.convert import Convert
from drivers.lidar.velodyne.proto.config import VelodyneConfig
from drivers.lidar.velodyne.proto.data_proto import VelodyneScan
from sub_modules.logger.logger import get_logger

convert_log = get_logger('velodyne_convert',True,'velodyne_convert.log',logging.WARNING,logging.INFO,'./logs/driver')

class VelodyneConvertComponent:
    def __init__(self, config: VelodyneConfig):
        self.config = config
        self.conv = Convert(config)
        
    def process(self, scan_msg: VelodyneScan, pcd_out):
        if pcd_out.empty():
            convert_log.warning(f"point_cloud_out is emmty")
        
        pcd_out.clear()
        self.conv.convert_packets_to_pointcloud(scan_msg, pcd_out)

        if pcd_out.empty():
            convert_log.warning(f"point_cloud_out convert is empty.")
        
        return True