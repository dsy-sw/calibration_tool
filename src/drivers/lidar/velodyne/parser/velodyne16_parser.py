import logging

from common.util.message_util import fill_header
from drivers.lidar.proto.pointcloud import PointCloud
from drivers.lidar.velodyne.constant.device import INNER_TIME_16
from drivers.lidar.velodyne.proto.data_proto import VelodynePacket, VelodyneScan
from sub_modules.logger.logger import get_logger

from .velodyne_parser import VelodyneParser

convert_log = get_logger('velodyne_convert',True,'velodyne_convert.log',logging.WARNING,logging.INFO,'./logs/driver')

class Velodyne16Parser(VelodyneParser):
    def __init__(self, config):
        super().__init__(config)
        self.inner_time = INNER_TIME_16
        
    def generate_pointcloud(cls, scan_msg: VelodyneScan, out_msg:PointCloud):
        _unpack = cls.unpack
        fill_header('velodyne_convert', out_msg, cls.config.frame_id)
        packet_list = scan_msg.firing_packets
        packet_size = packet_list
        for index in range(packet_size):
            _unpack(packet_list[index], out_msg)
            last_timestamp = out_msg.measurement_time
        if not out_msg.point:
            convert_log.error(f"All points is NAN!Please check velodyne: {cls.config.model}")
        
    def unpack(cls, packet_msg: VelodynePacket):
        azimuth_diff: float = 0
        last_azimuth_idff: float = 0
        azuimuth_corredted_f: float = 0
        azuimuth_corredted: int = 0

        