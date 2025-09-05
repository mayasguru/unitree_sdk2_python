from dataclasses import dataclass
from cyclonedds.idl import IdlStruct
import cyclonedds.idl.types as types


# This class defines user data consisting of a float data and a string data
@dataclass
class Image(IdlStruct, typename="Image"):
    image_data: types.sequence[types.uint8]