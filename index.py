import logging.config
import os

logging.config.fileConfig(os.getcwd() + '/logging.conf')
logger = logging.getLogger('scrapper')


def main():
    logger.info("test logger")


if __name__ == '__main__':
    main()
