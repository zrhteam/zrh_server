import os


class Config:
    # 使用导入的os模块来生成随机秘钥,此秘钥用于Flask中的session。
    SECRET_KEY = os.urandom(24)

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://data2:zruih2ZRH@!@47.92.250.148/riskapply'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbgroup:db123456@10.20.5.110/zrh_data'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test_db:zrhdb123456@124.71.45.84:33060/zrh_data'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 同上
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://data2:zruih2ZRH@!@47.92.250.148/riskapply'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'default': TestingConfig,
    'testing': TestingConfig
}
