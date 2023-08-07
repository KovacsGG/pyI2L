import csv



class CSVReader():
    def __init__(self, file, quoting = csv.QUOTE_ALL, quotechar='"'):
        self.reader = csv.reader(file, quoting=csv.QUOTE_NONE)
        self.strip = quoting == csv.QUOTE_ALL
        self.quotechar = quotechar
        self.doublequote_escape_char = "\ue011"

    def encode_doublequotes(self, s: str):
        if s == '""': return s
        while s.find(self.doublequote_escape_char) != -1:
            self.doublequote_escape_char *= 2
        count = 0
        for c in s:
            if c == self.quotechar:
                count += 1
            else:
                break
        if not count % 2:
            s = s.replace(self.quotechar * 2, self.doublequote_escape_char)
        else:
            s = self.quotechar + s[1:].replace(self.quotechar * 2, self.doublequote_escape_char)
        return s

    def decode_doublequotes(self, s: str):
        return s.replace(self.doublequote_escape_char, self.quotechar)
    
    def strip_quotes(self, s: str):
        return s.removesuffix(self.quotechar).removeprefix(self.quotechar)

    def __iter__(self):
        return self

    def __next__(self):
        out = []
        part = ""
        while True:
            row = next(self.reader)
            if row == []:
                part += "\n"
                continue
            for i in row:
                encoded = self.encode_doublequotes(i)
                part += encoded
                if not part.startswith(self.quotechar):
                    out.append(self.decode_doublequotes(part))
                    part = ""
                    continue
                if part.endswith(self.quotechar):
                    out.append(self.decode_doublequotes(self.strip_quotes(part) if self.strip else part))
                    part = ""
                    continue
                else:
                    if i == row[-1]:
                        part += "\n"
                    else:
                        part += self.reader.dialect.delimiter
                    continue
            if part == "": break
        return out