from dataclasses import dataclass
from cyclonedds.idl import IdlStruct
import cyclonedds.idl.types as types


IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
RGB_CHANNELS = 3
PIXEL_DATA_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT * RGB_CHANNELS

# This class defines user data consisting of a float data and a string data
@dataclass
class Image(IdlStruct, typename="Image"):
    image_data: types.array[types.uint8, PIXEL_DATA_SIZE]