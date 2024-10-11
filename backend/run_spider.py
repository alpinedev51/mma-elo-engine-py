import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from scrapy.cmdline import execute

if __name__ == '__main__':
    execute(['scrapy', 'crawl', 'ufc_spider'])