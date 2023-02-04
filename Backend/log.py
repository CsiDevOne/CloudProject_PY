import logging


class Log:

    def __init__(self, path):
        self.path = path

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.handler = logging.FileHandler(self.path)
        self.handler.setLevel(logging.INFO)

        self.formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)

        self.logger.addHandler(self.handler)

    def __del__(self):
        self.handler.close()

    def clear_logs(self):
        with open(self.path, 'w+') as f:
            if len(f.read()) > 10000:
                f.write('\n < logs got cleared > \n')
                f.close()