import json


class JSONHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def open_file(self, operation="r"):
        return open(self.file_path, operation)

    def read_file(self):
        opened_file = self.open_file("r")
        file_data = json.load(opened_file)
        self.close_file(opened_file)
        return file_data

    def write_file(self, data):
        opened_file = self.open_file("w")
        opened_file.write(json.dumps(data, indent=4))
        self.close_file(opened_file)

    def close_file(self, opened_file):
        opened_file.close()
