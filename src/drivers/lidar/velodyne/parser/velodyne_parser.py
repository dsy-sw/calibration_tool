from drivers.lidar.proto.pointcloud import PointXYZIT
from drivers.lidar.velodyne.parser.velodyne16_parser import Velodyne16Parser
from drivers.lidar.velodyne.parser.velodyne32_parser import Velodyne32Parser
from drivers.lidar.velodyne.proto.config import VelodyneConfig
from sub_modules.util.common.extentions import LoadFileByExtension

common_config_path = './src/drivers/lidar/velodyne/config/config.json'
calibration_path = LoadFileByExtension.get_data(common_config_path)['path']['calibration']

class VelodyneParser:
    def __init__(self, config: VelodyneConfig):
        self.config = config
        self.calibration = LoadFileByExtension.get_data(calibration_path[self.__class__])

    def get_none_point(self, timestamp: float):
        return PointXYZIT(None, None, None, 0, timestamp)

    def generate_pointcloud(self):  # override 필수
        raise NotImplementedError

    def order(self, pcd):  # override 필수
        raise NotImplementedError


class VelodyneParserFactory:
    def create_parser(config: VelodyneConfig):
        _model = config.model.name
        match _model:
            case "VLP16":
                return Velodyne16Parser(config)
            case "VLP32C":
                return Velodyne32Parser(config)