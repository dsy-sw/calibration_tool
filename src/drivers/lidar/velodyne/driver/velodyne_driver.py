import logging
import socket
from collections import deque
from datetime import datetime
from struct import unpack
from time import time, time_ns

from common.util.message_util import fill_header
from drivers.lidar.velodyne.constant.device import (
    FIRING_DATA_PACKET_SIZE,
    POSITIONING_DATA_PACKET_SIZE,
)
from drivers.lidar.velodyne.proto.config import VelodyneConfig
from drivers.lidar.velodyne.proto.data_proto import (
    NMEATime,
    VelodyneInfo,
    VelodynePacket,
    VelodyneScan,
)
from sub_modules.bridge.socket.socket import SOCKET_KIND, get_logger, get_socket

driver_log = get_logger('velodyne_driver',True,'velodyne_driver.log',logging.WARNING,logging.INFO,'./logs/driver')


class VelodyneDriver:
    def __init__(self, config: VelodyneConfig):
        self.config = config
        self.scan_data = VelodyneScan(firing_packets=deque([],maxlen=config.npacket))
        self.scan_data.model = config.model.name
        self.nmea_time = NMEATime()
        self.input_sock = socket.socket(type=socket.SOCK_DGRAM)
        self.input_sock.bind('',config.firing_data_port)
        self.input_sock.timeout(1)
        self.positioning_sock = socket.socket(type=socket.SOCK_DGRAM)
        self.positioning_sock.bind('',config.positioning_data_port)
        self.positioning_sock.timeout(1)
        # self.input_sock = get_socket(SOCKET_KIND.UDP,'input_sock',time(),'',config.firing_data_port,'localhost',0,receive_callback=self.get_firing_data_packet,buffer=FIRING_DATA_PACKET_SIZE)
        # self.positioning_sock = get_socket(SOCKET_KIND.UDP,'input_sock',time(),'',config.positioning_data_port,'localhost',0,receive_callback=self.get_positioning_data_packet,buffer=POSITIONING_DATA_PACKET_SIZE)

    def poll(self, scan: VelodyneScan):
        _config = self.config
        poll_result = self.poll_standard(scan)
        if poll_result == False or poll_result == -1:  # 오류 정의 필요
            return False
        
        if not scan.firing_packets:
            driver_log.info(f"Get an empty scan from port: {_config.firing_data_port}")
            return False

        fill_header('velodyne_driver', scan, _config.frame_id)
        scan.model = _config.model.name
        scan.mode = _config.mode.name
        
    
    def poll_standard(self, scan: VelodyneScan):
        _npacket = self.config.npacket
        count = 0
        _get_data_packet = self.get_data_packet
        while count < _npacket:
            while  1:
                packet = VelodynePacket()
                rc = _get_data_packet(packet)
                if rc == 0:
                    scan.firing_packets.append(packet)
                    break
                elif rc < 0:
                    return rc
                count+=1
                
        return 0

    def get_data_packet(self, packet: VelodynePacket):
        time1 = time_ns()
        try:
            raw_packet, client_addr = self.input_sock.recvfrom(FIRING_DATA_PACKET_SIZE)
            if len(raw_packet) == FIRING_DATA_PACKET_SIZE:
                packet.data = raw_packet
            driver_log.error(f"Incomplete Velodyne rising data packet read: {len(raw_packet)}, bytes from {client_addr}") 
        except socket.timeout:
            return -2
        packet.stamp = (time_ns()-time1)/2
        return 0
        
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