from io import BufferedIOBase, BytesIO
from ..I2 import I2
ext = ".dat"



def Reader(file: str):
    with open(file, "rb") as f:
        data = BytesIO(f.read())
    return data
    
class Writer:
    def __init__(self, data: I2):
        self.data = data
    
    def to_bytes(self):
        return self.data.to_bytes()