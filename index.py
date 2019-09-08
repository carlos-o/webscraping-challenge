import logging.config
from os import getcwd
from scraper import init_scraper

# obtain root project
logging.config.fileConfig(getcwd() + '/logging.conf')
logger = logging.getLogger('scrapper')


def main():
    init_scraper()


if __name__ == '__main__':
    main()
