import os
import logs.logger as log

BROKEN_LINK_CODE=815

def get_size(start_path, app_code=log.MOVIES):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except OSError:
                l = log.logger(app_code)
                l.warning("Broken link found at %s"%(fp), BROKEN_LINK_CODE)
                
    return total_size
