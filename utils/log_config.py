import logging
import time
import os
from utils.settings import LOG_PATH

# 日志保存路径
log_path = LOG_PATH


class Log(object):
    def __init__(self):
        # log文件命名
        rq = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
        self.logname = log_path + rq + '.log'
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a')     # 追加模式
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message, exc_info=True)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


if __name__ == '__main__':
    log = Log()
    try:
        result = 10/0
    except Exception:
        log.error('Faild to get result')