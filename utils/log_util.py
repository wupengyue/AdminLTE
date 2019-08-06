from datetime import datetime
from datetime import timedelta
import os
import sys
import traceback
import logging

LOGGING_FORMAT = '%(asctime)s %(levelname)7s: %(filename)s:%(lineno)s[%(funcName)s]-> %(message)s'
__TIME_FMT = '%Y%m%d-%H%M%S'
__START_TIME = datetime(1970, 1, 1)
FILE_HANDLER = None


def init_logging(log_name=None, level=logging.INFO):
    # logging.basicConfig( level=level, format=LOGGING_FORMAT )
    global FILE_HANDLER
    logger = logging.getLogger()
    if isinstance(level, str):
        level = cvt_debug_level(level)

    logger.setLevel(level)
    formatter = logging.Formatter(LOGGING_FORMAT)

    for handler in logger.handlers:
        logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if log_name:
        log_dir = os.path.dirname(log_name)
        if os.path.exists(log_dir):
            handler = logging.handlers.RotatingFileHandler(log_name, 'a', 1024 * 1024, 20)
        else:
            handler = logging.FileHandler(log_name)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        FILE_HANDLER = handler


def cvt_debug_level(debugLevel):
    logLevel = logging.INFO
    if debugLevel == 'debug':
        logLevel = logging.DEBUG
    elif debugLevel == 'warn':
        logLevel = logging.WARN
    elif debugLevel == 'error':
        logLevel = logging.ERROR

    return logLevel


def set_debug_level(debugLevel):
    logLevel = cvt_debug_level(debugLevel)
    if logLevel is not None:
        init_logging(None, logLevel)


def std_fmt_name(fmtName):
    if fmtName.startswith('$'):
        nstr = fmtName[1:len(fmtName)]
        if nstr[0] == '-':
            nstr = nstr.replace('-', '_')
        fmtName = '_commonVal' + nstr
    return fmtName


def strptime(tstr, fmt):
    return datetime.strptime(tstr, fmt)


def total_seconds(dtime):
    delta = dtime - __START_TIME
    return delta.total_seconds()


def to_datetime(seconds):
    return __START_TIME + timedelta(0, seconds)


def delta_time(dtime1, dtime2):
    delta = dtime2 - dtime1
    return delta.total_seconds()


def str_time(dtime, fmt=__TIME_FMT):
    return datetime.strftime(dtime, fmt)


def time_str(tstr, fmt=__TIME_FMT):
    return strptime(tstr, fmt)


def seconds_str(tstr, fmt=__TIME_FMT):
    dtime = strptime(tstr, fmt)
    return total_seconds(dtime)


def str_seconds(seconds, fmt=__TIME_FMT):
    dtime = to_datetime(seconds)
    return str_time(dtime, fmt)


def cur_time():
    now = datetime.now()
    return now


def cur_timestr(fmt=__TIME_FMT):
    now = datetime.now()
    return str_time(now, fmt)


def mkdir(dname):
    logging.debug('try make directory:' + dname)
    try:
        if not os.path.exists(dname):
            os.makedirs(dname)
        return True
    except:
        logging.error('\n' + traceback.format_exc())
        logging.error('create directory:' + dname + ' failed')
        return False


def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def raise_virtual(func):
    raise Exception('derived must implement ' + func + ' virtual function')
