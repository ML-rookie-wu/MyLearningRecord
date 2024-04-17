import os


class MapParser:

    def __init__(self, map_file):
        self.cwd = os.path.split(__file__)[0]
        self.map_file_name = map_file
        self.cmd_addr = None
        self.api_dict = {}

        self.extract_cmd_addr()
        self.extract_api_dict()
        self.extract_var_dict()

    def extract_cmd_addr(self):
        pass

    def extract_api_dict(self):
        pass

    def extract_var_dict(self):
        pass
