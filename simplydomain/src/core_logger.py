import logging


class CoreLogging(object):
    """simple logging testing and dev"""

    def __init__(self):
        self.name = ".simplydomain.log"

    def start(self, level=logging.INFO):
        logger = logging.getLogger("simplydomain")
        logger.setLevel(level)
        fh = logging.FileHandler(self.name)
        formatter = logging.Formatter(
            '%(asctime)s-[%(name)s]-[%(levelname)s]- %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info("Program started")
        logging.captureWarnings(True)
        logger.info("Set Logging Warning Capture: True")

    def debugmsg(self, message, modulename):
        try:
            msg = 'simplydomain.' + str(modulename)
            logger = logging.getLogger(msg)
            logger.debug(str(message))
        except Exception as e:
            print(e)

    def infomsg(self, message, modulename):
        try:
            msg = 'simplydomain.' + str(modulename)
            logger = logging.getLogger(msg)
            logger.info(str(message))
        except Exception as e:
            print(e)

    def warningmsg(self, message, modulename):
        try:
            msg = 'simplydomain.' + str(modulename)
            logger = logging.getLogger(msg)
            logger.warning(str(message))
        except Exception as e:
            print(e)
