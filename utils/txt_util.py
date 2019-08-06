import os
import uuid
import logging


class TextFileUtil:
    def __init__(self):
        self.uuid = str(uuid.uuid4())

    def update_file(self, path, fields):
        org_file = open(path, 'r')
        new_file_path = '/tmp/' + os.path.basename(path) + '.' + self.uuid
        new_file = open(new_file_path, 'w')
        try:
            contents = org_file.read()
            logging.debug('before update: ' + str(contents))
            for field in fields:
                logging.debug('field: ' + str(field))
                contents = contents.replace(field['org'], field['upd'])
            logging.debug('after update: ' + str(contents))
            new_file.write(contents)
        except IOError:
            new_file_path = None
        finally:
            org_file.close()
            new_file.close()
        logging.debug(new_file_path)
        return new_file_path

    def dump_file(self, path, contents):
        file = open(path, 'w')
        ret = True
        try:
            file.write(contents)
        except IOError:
            logging.error("Fail to dump file " + path)
            ret = False
        finally:
            file.close()
        return ret

    def remove_file(self, path):
        os.remove(path)
