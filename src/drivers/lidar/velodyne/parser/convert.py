import logging

from drivers.lidar.velodyne.parser.velodyne_parser import (
    VelodyneParser,
    VelodyneParserFactory,
)
from drivers.lidar.velodyne.proto.config import VelodyneConfig
from drivers.lidar.velodyne.proto.data_proto import VelodyneScan
from sub_modules.logger.logger import get_logger

convert_log = get_logger('velodyne_convert',True,'velodyne_convert.log',logging.WARNING,logging.INFO,'./logs/driver')

class Convert:
    def __init__(self, config: VelodyneConfig):
        self.config = config
        self.parser: VelodyneParser = VelodyneParserFactory.create_parser(config.model)
        
    def convert_packets_to_pointcloud(self, scan: VelodyneScan, pcd_out):
        self.parser.generate_pointcloud(scan, pcd_out)
        if pcd_out.empty():
            convert_log.error(f"Point cloud has no point")
            return
        
