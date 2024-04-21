



class AtsConfig:
    static_config = None
    dynamic_config = None
    initiated = False
    logger = None

    def __init__(self):
        self.static_config = None
        self.dynamic_config = None

    @staticmethod
    def add_more_config(src_path):
        pass

    @staticmethod
    def gen_runner_config():
        pass

    @staticmethod
    def load_static_config():
        pass

    @staticmethod
    def load_dynamic_config():
        pass

    @staticmethod
    def get_config():
        pass

    @staticmethod
    def get_logger(test_project, test_module):
        pass

    @staticmethod
    def del_logger():
        pass
