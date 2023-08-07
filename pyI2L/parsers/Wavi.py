from CSVReader import CSVReader



class Reader:
    def __init__(self, file):
        self.reader = CSVReader(file)
        self.languages = self.format_head(next(self.reader))

    def format_head(self, row: list[str]):
        langs = ["English", "en"]
        for s in row[4:]:
            (lang, code) = s.rsplit(" ", 1)
            lang = lang.rstrip()
            code = code[1:-1]
            langs.append(lang)
            langs.append(code)
        return langs

    def __iter__(self):
        return self
    
    def __next__(self):
        row = next(self.reader)
        return row[0:1] + row[3:]

