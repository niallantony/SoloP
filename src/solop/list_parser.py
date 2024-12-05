class ListParser:
    def __init__(self):
        pass

    def read_file(self, f):
        try:
            with open(f, 'r') as f:
                return print(f.read())
        except FileNotFoundError:
            print("File not found")