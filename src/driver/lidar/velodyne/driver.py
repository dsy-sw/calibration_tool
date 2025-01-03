import logging
from collections import deque
from datetime import datetime
from struct import unpack
from time import time, time_ns

from driver.lidar.velodyne.constant.device import (
    FIRING_DATA_PACKET_SIZE,
    POSITIONING_DATA_PACKET_SIZE,
)
from driver.lidar.velodyne.proto.config import VelodyneConfig
from driver.lidar.velodyne.proto.data_proto import (
    NMEATime,
    VelodyneInfo,
    VelodynePacket,
    VelodyneScan,
)
from sub_modules.bridge.socket.socket import SOCKET_KIND, get_logger, get_socket

driver_log = get_logger('velodyne_driver',True,'velodyne_driver',logging.WARNING,logging.INFO,'./logs/driver')


class VelodyneDriver:
    def __init__(self, config: VelodyneConfig):
        self.scan_data = VelodyneScan(firing_packets=deque([],maxlen=config.npacket))
        self.scan_data.model = config.model
        self.nmea_time = NMEATime()
        self.input_sock = get_socket(SOCKET_KIND.UDP,'input_sock',time(),'',config.firing_data_port,'localhost',0,receive_callback=self.get_firing_data_packet,buffer=FIRING_DATA_PACKET_SIZE)
        self.positioning_sock = get_socket(SOCKET_KIND.UDP,'input_sock',time(),'',config.positioning_data_port,'localhost',0,receive_callback=self.get_positioning_data_packet,buffer=POSITIONING_DATA_PACKET_SIZE)

    def get_firing_data_packet(self, raw_bytes: bytes, timestamp: float = None):
        _scan_data = self.scan_data
        if not raw_bytes:
            # _scan_data.firing_packets.clear()
            driver_log.error(f"Bytes data is empty.")
            return False
        if timestamp is None:
            timestamp = time_ns()
        pkt = VelodynePacket()

        if len(raw_bytes) == FIRING_DATA_PACKET_SIZE:
            pkt.data = raw_bytes
        else:
            driver_log.error(f"Firing data size of raw_bytes is {len(raw_bytes)} instead of {FIRING_DATA_PACKET_SIZE}.")
        
        pkt.stamp = (time_ns()+timestamp)/2
        _scan_data.firing_packets.append(pkt)
        _scan_data.timestamp = time()
        
        return True

    def get_positioning_data_packet(self, raw_bytes: bytes, timestamp: float = None):
        if len(raw_bytes) != POSITIONING_DATA_PACKET_SIZE:
            driver_log.warning(f"Positioning data size of raw_bytes is {len(raw_bytes)} instead of {POSITIONING_DATA_PACKET_SIZE}")
        if timestamp is None:
            timestamp = time_ns()
        
        _scan_data = self.scan_data
        _scan_data.positioning_packets = raw_bytes
        if _scan_data.basetime == 0 and self.exract_nmea_time_from_packet(self.nmea_time, raw_bytes[0xCE:0x14D]):
            self.set_basetime_from_nmeatime(self.nmea_time, _scan_data)
        _scan_data.velodyne_info = VelodyneInfo((time_ns()+timestamp)/2, *unpack("<BBBhIBBIBBBB",raw_bytes[0xBB:0xCE]))
    
    def exract_nmea_time_from_packet(self, nmea_time: NMEATime, nmea_raw_bytes: bytes):
        nmea_data = nmea_raw_bytes.decode("ascii").split(',')
        if nmea_data[0] == "$GPGGA":
            pass
        elif nmea_data[0] == "$GPRMC":
            nmea_time.day, nmea_time.mon, nmea_time.year = [int(nmea_data[9][i:i+2]) for i in range(0,len(nmea_data[9]),2)]
            nmea_time.hour, nmea_time.min, nmea_time.sec = [int(nmea_data[1][i:i+2]) for i in range(0,len(nmea_data[1]),2)]
        else:
            return False
        return True
        
    def set_basetime_from_nmeatime(self, nmea_time: NMEATime, scan_data: VelodyneScan):
        nmea_time.year += 2000
        scan_data.basetime = datetime(*nmea_time.__match_args__).timestamp()
        return True

class VelodyneDriverFactory:
    def create_driver(config: VelodyneConfig):
        driver = VelodyneDriver(config)

        return driver