import csv
from ..I2 import I2, Record, Field
ext = ".csv"



class Reader:
    def __init__(self, file):
        self.file = open(file, "r", encoding="utf-8", newline="")
        self.reader = csv.reader(self.file)
        self.padding = 16
        self.languages = self.format_head(next(self.reader))

    def format_head(self, row: list[str]):
        self.padding = int(row[0])
        langs = []
        for s in row[1:]:
            (lang, code, type) = s.rsplit(" ", 2)
            langs.append((lang.rstrip(), code[1:-1], int(type)))
        return langs

    def __iter__(self):
        return self
    
    def __next__(self):
        row = next(self.reader)
        row[-1] = int(row[-1])
        return row
    
    def __del__(self):
        self.file.close()
    
class Writer:
    def __init__(self, data: I2):
        self.data = data
    
    def languages(self):
        strings = ""
        for item in self.data.languages.items:
            strings += f',"{item[0]} [{item[1]}] {item[2]}"'
        return f'{self.data.body.padding}{strings}\n'
    
    def body(self):
        s = ""
        for r in self.data.body.items:
            s += self.record(r)
        return s
    
    def record(self, r: Record):
        strings = ""
        for read in r.items:
            strings += ',"' + self.field(read) + '"'
        return f'"{r.id}"{strings},{r.type}\n'
    
    def field(self, f: Field):
        return f.v.replace('"', '""')

    def to_bytes(self):
        return f"{self.languages()}{self.body()}".encode("utf-8")