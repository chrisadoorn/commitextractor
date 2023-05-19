# bedoelt voor analyse van de tekstachteraf aangezien dit een echt code bestand is


class ElixirParse:

    def __init__(self, path: str):
        self.path = path
        self.file = open(path, 'r')
        self.lines = self.file.readlines()
        self.file.close()

    def parse(self):
        for line in self.lines:
            if line.startswith('#'):
                continue
            else:
                if line.startswith('def'):
                    print(line)
                else:
                    continue