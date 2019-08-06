from io import BytesIO, StringIO
import yaml
from datetime import datetime
from datetime import timedelta
import os
import traceback
import logging
from tomorrow import threads
import concurrent.futures
import uuid


class BaseUtil():
    __TIME_FMT = '%Y%m%d-%H%M%S'
    __START_TIME = datetime(1970, 1, 1)

    @classmethod
    def bytes2str(cls, bstr):
        return bstr.decode('utf-8')

    @classmethod
    def str2bytes(cls, sstr):
        return sstr.encode('utf-8')

    @classmethod
    def str2io(cls, bstr):
        try:
            if isinstance(bstr, bytes):
                sio = BytesIO(bstr)
            else:
                sio = StringIO(bstr)

            return sio
        except Exception as e:
            logging.error('failed to convert to io object, str: ' + str(bstr) + ', with Exception: ' + str(e))
            return None

    @classmethod
    def loadYaml(cls, path):
        stream = open(path, 'r')
        config = yaml.load(stream)
        stream.close()
        return config

    @classmethod
    def dumpYaml(cls, path, config):
        with open(path, 'w') as fout:
            fout.write(yaml.dump(config, default_flow_style=False, indent=4, width=1000))

    @staticmethod
    def strptime(tstr, fmt):
        return datetime.strptime(tstr, fmt)

    @staticmethod
    def total_seconds(dtime):
        delta = dtime - BaseUtil.__START_TIME
        return delta.total_seconds()

    @staticmethod
    def to_datetime(seconds):
        return BaseUtil.__START_TIME + timedelta(0, seconds)

    @staticmethod
    def delta_time(dtime1, dtime2):
        delta = dtime2 - dtime1
        return delta.total_seconds()

    @staticmethod
    def str_time(dtime, fmt=__TIME_FMT):
        return datetime.strftime(dtime, fmt)

    @staticmethod
    def time_str(tstr, fmt=__TIME_FMT):
        return BaseUtil.strptime(tstr, fmt)

    @staticmethod
    def seconds_str(tstr, fmt=__TIME_FMT):
        dtime = BaseUtil.strptime(tstr, fmt)
        return BaseUtil.total_seconds(dtime)

    @staticmethod
    def cur_time():
        now = datetime.now()
        return now

    @staticmethod
    def cur_sec():
        now = BaseUtil.cur_time()
        return BaseUtil.total_seconds(now)

    @staticmethod
    def cur_timestr(fmt=__TIME_FMT):
        now = datetime.now()
        return BaseUtil.str_time(now, fmt)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def raise_virtual(func):
        raise Exception('derived must implement ' + func + ' virtual function')

    @staticmethod
    def tail_file(f, lines, blockSize=256):
        total_lines_wanted = lines

        BLOCK_SIZE = blockSize
        f.seek(0, 2)
        block_end_byte = f.tell()
        size = block_end_byte
        lines_to_go = total_lines_wanted
        block_number = -1
        blocks = []  # blocks of size BLOCK_SIZE, in reverse order starting
        # from the end of the file
        while lines_to_go > 0 and block_end_byte > 0:
            if (block_end_byte - BLOCK_SIZE > 0):
                # read the last block we haven't yet read
                print('=====', str(block_number))
                # f.seek(block_number*BLOCK_SIZE, 2)  #will not work for python 3
                f.seek(size + block_number * BLOCK_SIZE, 0)
                blocks.append(f.read(BLOCK_SIZE))
            else:
                # file too small, start from begining
                f.seek(0, 0)
                # only read what was not read
                blocks.append(f.read(block_end_byte))
            lines_found = blocks[-1].count('\n')
            lines_to_go -= lines_found
            block_end_byte -= BLOCK_SIZE
            block_number -= 1
        all_read_text = ''.join(reversed(blocks))
        # set the file point to the tail start
        f.seek(size - len(all_read_text), 0)
        return all_read_text.splitlines()[-total_lines_wanted:]

    @staticmethod
    @threads(20)
    def threading(func, *args, **kwargs):
        foo = type('TomorrowResult', (object,), {})()
        foo.result = func(*args, **kwargs)
        return foo

    def run_thread(func, *args, **kwargs):
        result = func(*args, **kwargs)
        return result

    @staticmethod
    def flatten(dictionary):
        stack = [((), dictionary)]
        result = {}
        while stack:
            path, current = stack.pop()
            for k, v in current.items():
                if isinstance(v, dict) and v:
                    stack.append((path + (k,), v))
                else:
                    result["/".join((path + (k,)))] = v or ""
        return result

    @staticmethod
    def parallel(numWorkers, runfunc, objList, *args, **kwargs):
        if numWorkers < 0:
            numWorkers = len(objList)
        if numWorkers == 0:
            return []

        resList = list()
        with concurrent.futures.ThreadPoolExecutor(max_workers=numWorkers) as executor:
            targets = {executor.submit(runfunc, obj, *args, **kwargs): obj for obj in objList}
            for future in concurrent.futures.as_completed(targets):
                try:
                    resList.append(future.result())
                except Exception as e:
                    traceback.print_exc()
                    logging.error('catched exception: ' + str(e) + ' with runfunc: ' + str(runfunc))

        return resList

    @staticmethod
    def genTmpFileName(prefix='', suffix=''):
        return '/tmp/%s%s%s' % (prefix, str(uuid.uuid4())[:6], suffix)

    @staticmethod
    def isLocalHost(host):
        return host in ['localhost', '127.0.0.1']

    @classmethod
    def rmFile(cls, path):
        return os.system('rm -f %s' % path)
