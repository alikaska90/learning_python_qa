from csv import DictReader


class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def open_file(self, operation="r"):
        return open(self.file_path, operation)

    def read_file(self):
        opened_file = self.open_file("r")
        try:
            file_data = [row for row in DictReader(opened_file)]
            return file_data
        finally:
            self.close_file(opened_file)

    def close_file(self, opened_file):
        opened_file.close()

