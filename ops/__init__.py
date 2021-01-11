from flask import Flask, render_template, request, session, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from conf.default import config

db = SQLAlchemy()


def app_create(config_name):
    from functions.init_data import init_data_blueprint
    from functions.login import login_blueprint
    from functions.headquarter_func import headquarter_blueprint
    from functions.region_func import region_blueprint
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(blueprint=init_data_blueprint)
    app.register_blueprint(blueprint=login_blueprint)
    app.register_blueprint(blueprint=headquarter_blueprint)
    app.register_blueprint(blueprint=region_blueprint)
    # 这里调用前面定义的配置文件的对象
    app.config.from_object(config[config_name])
    # 初始化配置
    config[config_name].init_app(app)
    # 初始化数据库,官方定义.
    db.init_app(app)
    return app
