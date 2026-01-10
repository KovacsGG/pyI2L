from collections.abc import Sequence
from io import BufferedIOBase


class UnityPyError(Exception):
    pass

class I2ParsingError(Exception):
    pass

def i2assert(src: BufferedIOBase, expect: bytearray | list[bytearray]):
    if not isinstance(expect, list):
        expect = [expect]
    fail = True
    found = src.read(len(expect[0]))
    for e in expect:
        fail = fail and found != e
    if fail:
        raise I2ParsingError(f"Expected {expect} at index {src.tell() - len(e)}, found {found}.")
    return found
