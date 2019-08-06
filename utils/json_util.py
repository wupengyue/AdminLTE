import json
import logging


class JsonUtil(object):
    # if set force=True, all field will be treated as string to be sorted
    @classmethod
    def ordered(cls, obj, force=False):
        if isinstance(obj, dict):
            return sorted((k, cls.ordered(v)) for k, v in obj.items())
        elif isinstance(obj, list):
            if not force:
                try:
                    # if Exception, means the list has its order, should not order here
                    return sorted(cls.ordered(x) for x in obj)
                except:
                    return obj
            else:
                return sorted(cls.ordered(x) for x in obj)

        else:
            if force:
                return str(obj)

    @classmethod
    # transform a json str to json format
    def json_str(cls, raw_json_str):
        raw_json_str = raw_json_str.strip()
        try:
            if raw_json_str[0] == '{' or raw_json_str[0] == '[':
                return json.loads(raw_json_str)
            else:
                return raw_json_str
        except Exception as e:
            logging.error('failed to parse json raw_json_str:' + str(raw_json_str) + ' with exception:' + str(e))
            return None

    @classmethod
    # transform a json format to json str
    def str_json(cls, obj, indent=None):
        return json.dumps(obj, indent=indent)

    @classmethod
    def load_json_file(cls, path):
        with open(path) as f:
            try:
                return json.load(f)
            except Exception as e:
                logging.error('failed to load json file: ' + path + ' with exception: ' + str(e))
                return None

    @classmethod
    def equal(cls, obj1, obj2):
        if type(obj1) == str:
            obj1 = cls.json_str(obj1)
            if not obj1:
                return False
        if type(obj2) == str:
            obj2 = cls.json_str(obj2)
            if not obj2:
                return False
        ordered_obj1 = cls.ordered(obj1)
        ordered_obj2 = cls.ordered(obj2)
        return ordered_obj1 == ordered_obj2

    @classmethod
    def contains(cls, obj1, obj2):
        if type(obj1) == str:
            obj1 = cls.json_str(obj1)
            if not obj1:
                return False
        if type(obj2) == str:
            obj2 = cls.json_str(obj2)
            if not obj2:
                return False

        if not isinstance(obj1, dict):
            logging.error('objtype is not matched, obj1: ' + str(type(obj1)) + ', obj2: ' + str(type(obj2)))
            return False

        if isinstance(obj2, dict):
            for k, v2 in obj2.items():
                if k not in obj1:
                    logging.debug('key: ' + k + ' is not in')
                    return False
                v1 = obj1[k]
                if not cls.equal(v1, v2):
                    logging.debug('objects not matched, v1: ' + str(v1) + ', v2: ' + str(v2))
                    return False
            return True
        else:
            logging.error(
                'objects contains only support dict, while type(obj1) is:' + str(type(obj1)) + ', type(obj2) is:' + str(
                    type(obj2)))
            return False
