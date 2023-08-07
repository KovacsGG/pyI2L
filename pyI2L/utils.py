from typing import BinaryIO



def align(i: int):
    """Return the requred number of padding bytes to be 4-byte aligned."""
    return (4 - i % 4) % 4


def to_i32(file: BinaryIO):
    """Read a 32bit int from a byte stream."""
    return int.from_bytes(file.read(4), "little")


def i32(i: int | list[int]) -> bytearray:
    """Return a 32bit bytearray encoding the given int. (Little endian)"""
    if isinstance(i, int):
        return bytearray(i.to_bytes(4, "little"))
    elif isinstance(i, list):
        b = bytearray()
        for x in i:
            b += i32(x)
        return b
    else:
        raise ValueError()
