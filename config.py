# encoding: utf-8
"""
@author:
@file: config.py
@time: 2017/7/13 16:39
"""
'''配置文件，后台一些需要的配置需要在这里进行配置'''
import os
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
jenkins_url = 'http://192.168.1.120:8080/'  # jenkins的地址
jenkins_user = 'admin'  # jenkins的用户名
jenkins_password = '1'  # jenkins的密码
system_request_toke = 'Fetext_token_system'  # 系统内部依赖接口请求的时候需要加个token来区分
Try_Num_Case = 5  # 重试的次数
Interface_Time_Out = 5000  # 超时时间
redis_password = '123456'
max_connec_redis = 10
test_fail_try_num = 3
jobstores = {
    'redis': RedisJobStore(),
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}
PageShow = 25  # 这里配置的就是每个页显示多少条数据
Dingtalk_access_token = ''  # 在这里配置您的接受通知的钉钉群自定义机器人webhook，
OneAdminCount = 10  # 设置项目管理员的数量
Config_daoru_xianzhi = 50  # 配置可以导入限制
save_duration = 24 * 60 * 60  # 配置redis存储的时长
redis_host = 'localhost'
redis_port = 6379
redis_save_result_db = 2


class dev(object):  # 研发环境配置
    SECRET_KEY = 'BaSeQuie'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    UPLOAD_FOLDER = '/upload'
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass


class test(object):  # 测试环境的配置
    SECRET_KEY = 'BaSeQuie'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.sqlite")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    UPLOAD_FOLDER = '/upload'
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass


class produce(object):  # 线上环境的配置
    SECRET_KEY = 'ProduceFXTest'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "produce.sqlite")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    UPLOAD_FOLDER = '/upload'
    DEBUG = False

    @staticmethod
    def init_app(app):
        pass


def lod():
    return dev


class Config(object):
    JOBS = []
    SCHEDULER_API_ENABLED = True
