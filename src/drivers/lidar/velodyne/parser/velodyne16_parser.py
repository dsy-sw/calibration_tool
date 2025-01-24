import logging
from struct import unpack

from common.util.message_util import fill_header
from drivers.lidar.proto.pointcloud import PointCloud
from drivers.lidar.velodyne.constant.velodyne_packet import *
from drivers.lidar.velodyne.proto.data_proto import *
from sub_modules.logger.logger import get_logger

from .velodyne_parser import VelodyneParser

module_name = 'velodyne_convert'
convert_log = get_logger(module_name,True,f'{module_name}.log',logging.WARNING,logging.INFO,'./logs/driver')

class Velodyne16Parser(VelodyneParser):
    def __init__(self, config):
        super().__init__(config)
        self.inner_time = INNER_TIME_16
        
    def generate_pointcloud(cls, scan_msg: VelodyneScan, out_msg:PointCloud):
        _unpack = cls.unpack
        fill_header(module_name, out_msg, cls.config.frame_id)
        packet_list = scan_msg.firing_packets
        packet_size = len(packet_list)
        for index in range(packet_size):
            _unpack(packet_list[index], out_msg)
            last_timestamp = out_msg.measurement_time
        if not out_msg.point:
            convert_log.error(f"All points is NAN!Please check velodyne: {cls.config.model}")
        
    def unpack(cls, packet_msg: VelodynePacket):
        azimuth_diff: float = 0
        last_azimuth_diff: float = 0
        azuimuth_corredted_f: float = 0
        azuimuth_corredted: int = 0

        raw_packets = packet_msg.data  # 1206bytes 데이터
        basetime = packet_msg.stamp
        block_packets = [raw_packets[packet:packet+BLOCK_SIZE] for packet in range(0,len(raw_packets),BLOCK_SIZE)]

        for block_num, block_packet in enumerate(block_packets):
            raw_block = RawBlock(block_packet, block_id=block_num)
            if block_num < BLOCKS_PER_PACKET-1:
                azimuth_diff = \
                    (36000+unpack(AZIMUTH_PACKET_FORMAT,
                    block_packets[block_num+1][FLAG_PACKET_SIZE:
                        FLAG_PACKET_SIZE+AZIMUTH_PACKET_SIZE])[0]-raw_block.rotation)%36000
                last_azimuth_diff = azimuth_diff
            else:
                azimuth_diff = last_azimuth_diff
                
            for firing_num in range(VLP16_FIRINGS_PER_BLOCK):
                for channel_id in range(VLP16_SCANS_PER_FIRING):
                    RawLaser()