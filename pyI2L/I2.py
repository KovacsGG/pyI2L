from .utils import i32, to_i32, align

from typing import Optional
from collections.abc import Iterator, Sequence
from io import BufferedIOBase


class Field:

    """Simpled value of I2 Localization"""

    def __init__(self, src: BufferedIOBase | str):
        """Constructs a value from byte stream or string.
        The byte stream should start at the length int of the value.
        A multiple of 4 bytes will be read.
        """
        if isinstance(src, BufferedIOBase):
            self.span = to_i32(src)
            self.v = src.read(self.span).decode("utf-8")
            self.padding = align(self.span)
            assert src.read(self.padding) == bytes(self.padding)
        elif isinstance(src, str):
            self.v = src
            self.span = len(self.v.encode("utf-8"))
            self.padding = align(self.span)
        else:
            raise TypeError()

    def __str__(self):
        return self.v
    
    def to_bytes(self):
        return (
            i32(self.span) + 
            bytearray(self.v, encoding="utf-8") +
            bytearray(self.padding)
        )


class Record:

    """Keyed array of I2 Localization strings."""

    def __init__(self, src: BufferedIOBase | Sequence[str]):
        """Constructs Record from byte stream or list of strings.
        The byte stream should start at the item-count int of the key of the record.
        The list should be formatted as [key, val0, val1, ...].
        """
        self.items: list[Field] = []
        if isinstance(src, BufferedIOBase):
            self.id = Field(src)
            assert src.read(4) == bytes(4)
            self.length = to_i32(src)
            for _ in range(self.length):
                self.items.append(Field(src))
            assert to_i32(src) == self.length
            assert src.read(24) == bytes(24)
        elif isinstance(src, Sequence):
            self.id = Field(src[0])
            self.length = len(src) - 1
            for i in src[1:]:
                self.items.append(Field(i))
        else:
            raise TypeError()            
    
    def __str__(self):
        """Return string representation formatted as a row of Crowdin-flavored CSV.
            "{id}","Text","","{item[0]}","{item[1]}",...\\n
        Quotechars in values are doubled.
        """
        strings = ""
        for read in self.items:
            strings += ',"' + str(read).replace('"', '""') + '"'
        return f'"{self.id}","Text",""{strings}\n'
    
    def to_bytes(self):
        items = bytearray()
        for i in self.items:
            items += i.to_bytes()
        return (
            self.id.to_bytes() +
            bytearray(4) +
            i32(self.length) +
            items +
            i32(self.length) +
            bytearray(24)
        )


class Header:
    
    """I2 Localization preamble."""
    
    def __init__(self, src: Optional[BufferedIOBase] = None):
        """Construct Header from optional byte stream
        Byte streams will be expected to equal a particular pattern.
        If no source is provided, the known pattern will be used.
        """
        if src is not None:
            assert src.read(12) == i32([0, 0, 1])
    
    def to_bytes(self):
        return i32([0, 0, 1])


class Body:

    """Container of I2 Localization Records"""

    def __init__(self, src: BufferedIOBase | Iterator[Sequence[str]]):
        """Contruct Body from byte stream or iterator.
        The byte stream should start at the item-count int of the container.
        The iterator should return list of strings in a format compatible with Record.__init__().
        """
        self.items: list[Record] = []
        if isinstance(src, BufferedIOBase):
            self.length = to_i32(src)
            for _ in range(self.length):
                self.items.append(Record(src))
        elif isinstance(src, Iterator):
            self.length = 0
            for r in src:
                self.length += 1
                self.items.append(Record(r))
        else:
            raise TypeError()
    
    def __str__(self):
        """Return string representation formatted as a heading-less Crowdin-flavored CSV.
            "{id}","Text","","{item[0]}","{item[1]}",...\\n
            ...
        Quotechars in values are doubled.
        """
        s = ""
        for r in self.items:
            s += str(r)
        return s
    
    def to_bytes(self):
        items = bytearray() 
        for r in self.items:
            items += r.to_bytes()
        return i32(self.length) + items


class Languages:

    """Language enumeration of I2 Localization."""

    def __init__(self, src: BufferedIOBase | Sequence[str]):
        """Construct language enumeration from byte stream or list of strings.
        The byte stream should start with int32[0, 1, 0] pattern preceding item-count int.
        The list should be formatted as [lang0.name, lang0.code, lang1.name, lang1.code, ...].
        """
        self.items: list[Field] = []
        if isinstance(src, BufferedIOBase):
            assert src.read(12) == i32([0, 1, 0])
            self.length = to_i32(src)
            for _ in range(self.length):
                self.items.append(Field(src))
                self.items.append(Field(src))
                assert src.read(4) == bytes(4)
        elif isinstance(src, Sequence):
            self.length = len(src) // 2
            for i in src:
                self.items.append(Field(i))
        else:
            raise TypeError()
        
    def __str__(self):
        """Return string representation formatted as the header of a Crowdin-falvored CSV.
            "Key","Type","Desc","{lang[0].name} {lang[0].code}","{lang[1].name} {lang[1].code}",...\\n
        """
        strings = ',"English"'
        for i in range(2, len(self.items), 2):
            strings += f',"{self.items[i]} [{self.items[i + 1]}]"'
        return f'"Key","Type","Desc"{strings}\n'
    
    def to_bytes(self):
        items = bytearray()
        for i in range(0, len(self.items), 2):
            items += self.items[i].to_bytes() + self.items[i + 1].to_bytes() + bytearray(4)
        return (i32([0, 1, 0]) +
                i32(self.length) +
                items +
                bytearray(24) + i32([3, 2, 1]) + bytearray(8)
        )
    
class I2:

    """I2 Localization table"""

    def __init__(self, src: BufferedIOBase | Iterator[Sequence[str]]):
        """Contruct table from byte stream or CSV iterator.
        The iterator should havea a languages attribute of a list of strings:
            [lang0.name, lang0.code, lang1.name, lang1.code, ...]
        It should iterate on a list of strings for every (logical) row of CSV.
        The fields should be formatted as:
            [key0, val0.0, val0.1, ...]
            [key1, val1.0, val1.1, ...]
            ...
        """
        if isinstance(src, BufferedIOBase):
            self.header = Header(src)
            self.body = Body(src)
            self.languages = Languages(src)
        elif isinstance(src, Iterator) and hasattr(src, "languages"):
            self.languages = Languages(src.languages) #type: ignore
            self.body = Body(src)
            self.header = Header()
        else:
            raise TypeError()

    def __str__(self):
        """Returns string representation formatted as a Crowdin-flavored CSV.
        Quotechars are doubled.
        """
        return f"{self.languages}{self.body}"
    
    def to_bytes(self):
        return (
            self.header.to_bytes() +
            self.body.to_bytes() +
            self.languages.to_bytes()
        )
