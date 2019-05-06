class FileReader:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        try:
            with open(self.file_name) as f:
                result = f.read()
        except IOError:
            result = ''
        return result
