

from time import time

from src.common.proto.message import Header


def fill_header(module_name: str, message: Header, frame_id = '') -> None:

    message.timestamp = time()
    message.module_name = module_name
    message.sequence_num += 1

    return True

def fill_header(module_name: str, message, frame_id = '') -> None:

    header:Header = message.header
    header.timestamp = time()
    header.module_name = module_name
    header.sequence_num += 1

    return True