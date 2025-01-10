from dataclasses import dataclass


@dataclass
class Header:
    timestamp: float = 0  # message publishing time in sec
    module_name: str = ''
    sequence_num: int = 0
    status: int = 0
    frame_id: str = ''