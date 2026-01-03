import csv
from ..I2 import I2, Record, Field
ext = ".csv"



class Reader:
    def __init__(self, file):
        self.file = open(file, "r", encoding="utf-8", newline="")
        self.reader = csv.reader(self.file)
        self.languages = self.format_head(next(self.reader))
        self.padding = 24

    def format_head(self, row: list[str]):
        langs = [("English", "en", 0)]
        for s in row[4:]:
            (lang, code) = s.rsplit(" ", 1)
            langs.append((lang.rstrip(), code[1:-1], 0))
        return langs

    def __iter__(self):
        return self
    
    def __next__(self):
        row = next(self.reader)
        return row[0:1] + row[3:] + [0] 
    
    def __del__(self):
            self.file.close()

class Writer:
    def __init__(self, data: I2):
        self.data = data
    
    def languages(self):
        strings = '"English"'
        for item in self.data.languages.items[1:]:
            strings += f',"{item[0]} [{item[1]}]"'
        return f'"Key","Type","Desc",{strings}\n'
    
    def body(self):
        s = ""
        for r in self.data.body.items:
            s += self.record(r)
        return s
    
    def record(self, r: Record):
        strings = ""
        for read in r.items:
            strings += ',"' + self.field(read) + '"'
        return f'"{r.id}","Text",""{strings}\n'
    
    def field(self, f: Field):
        return f.v.replace('"', '""')

    def to_bytes(self):
        return f"{self.languages()}{self.body()}".encode("utf-8")