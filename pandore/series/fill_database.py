import os
from series.series_processor import SeriesDirectoryProcessor

SERIES_DIR = '/data/vip/Series'

processor = SeriesDirectoryProcessor()
for d in [os.path.abspath(SERIES_DIR+'/'+dir) for dir in os.listdir(SERIES_DIR)
          if os.path.isdir(SERIES_DIR+'/'+dir)]:
    processor.process(d)
