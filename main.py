import copy
import datetime
import os,sys

from scrapy.cmdline import execute

if __name__ == '__main__':
    base_dir=os.path.dirname(os.path.abspath(__file__))
    sys.path.append(base_dir)
    execute(["scrapy","crawl","qcc"])





