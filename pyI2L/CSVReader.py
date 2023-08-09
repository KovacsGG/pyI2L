from io import BytesIO
from enum import IntEnum

__all__ = ["CSVReader"]

class States(IntEnum):
    START = 0
    QSTART = 1
    QUOT = 2
    QEND = 3
    UNQUOT = 4
    DBLQUOT_START = 5


class CSVReader():
    def __init__(self, data: bytes, sep = b",", quotechar= b'"'):
        data.replace(b"\r\n", b"\n")
        data.replace(b"\r", b"\n")
        self.bytes: BytesIO = BytesIO(data)
        self.sep: bytes = sep
        self.quot: bytes = quotechar

    def __iter__(self):
        return self

    def __next__(self):
        state = States.START
        out: list[str] = []
        field = bytearray()
        # Transitions: \n, sep, quotechar, alpha (other)
        while byte := self.bytes.read(1):
            if state == States.START:
                if byte == self.sep:
                    out.append(field.decode("utf-8"))
                    field = bytearray()
                elif byte == b"\n":
                    out.append(field.decode("utf-8"))
                    break
                elif byte == self.quot:
                    state = States.QSTART
                else:
                    field += byte
                    state = States.UNQUOT
            elif state == States.QSTART:
                if byte == self.quot:
                    state = States.DBLQUOT_START
                else:
                    field += byte
                    state = States.QUOT
            elif state == States.QUOT:
                if byte == self.quot:
                    state = States.QEND
                else:
                    field += byte
            elif state == States.QEND:
                if byte == self.quot:
                    field += byte
                    state = States.QUOT
                elif byte == self.sep:
                    out.append(field.decode("utf-8"))
                    field = bytearray()
                    state = States.START
                elif byte == b"\n":
                    out.append(field.decode("utf-8"))
                    break
                else:
                    raise ValueError(f'Malformed CSV: Expected \
                                      "{self.quot}", "{self.sep}" or "\\n" \
                                      but read "{byte}".')
            elif state == States.UNQUOT:
                if byte == self.sep:
                    out.append(field.decode("utf-8"))
                    field = bytearray()
                    state = States.START
                elif byte == b"\n":
                    out.append(field.decode("utf-8"))
                    break
                else:
                    field += byte
            elif state == States.DBLQUOT_START:
                if byte == self.sep:
                    out.append("")
                    state = States.START
                elif byte == b"\n":
                    out.append("")
                    break
                elif byte == self.quot:
                    field += byte
                    state = States.QUOT
                else:
                    field += self.quot
                    field += byte
                    state = States.UNQUOT

        if out == [] and byte == b'':
            raise StopIteration()
        return out