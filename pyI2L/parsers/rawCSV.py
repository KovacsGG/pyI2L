from ..CSVReader import CSVReader
from ..I2 import I2
ext = ".csv"



class Reader:
    def __init__(self, file):
        with open(file, "rb") as f:
            data = f.read()
        self.reader = CSVReader(data)
        self.languages = self.format_head(next(self.reader))

    def format_head(self, row: list[str]):
        langs = []
        for s in row[2:]:
            (lang, code) = s.rsplit(" ", 1)
            lang = lang.rstrip()
            code = code[1:-1]
            langs.append(lang)
            langs.append(code)
        return langs

    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.reader)
    
class Writer:
    def __init__(self, data: I2):
        self.data = data
    
    def __str__(self):
        return str(self.data)