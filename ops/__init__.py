from flask import Flask, render_template, request, session, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from conf.default import config
from flask_apscheduler import APScheduler  # as _BaseAPScheduler

scheduler = APScheduler()
db = SQLAlchemy()
db.session.expire_on_commit = False


def app_create(config_name):
    from functions.init_data import init_data_blueprint
    from functions.login import login_blueprint
    from functions.headquarter_func import headquarter_blueprint
    from functions.region_func import region_blueprint
    from functions.project_func import project_blueprint
    from functions.check_func import check_blueprint
    from functions.analyze_func import analyze_blueprint
    from functions.data_insight import insight_blueprint
    from functions.check_large_screen import check_ls_blueprint
    from functions.project_large_screen import project_ls_blueprint
    from functions.region_large_screen import region_ls_blueprint
    from functions.headquarter_large_screen import headquarter_ls_blueprint
    from functions.data_insight_func import insight_func_blueprint
    from functions.province_info_func import province_info_blueprint
    from functions.check_major_ls import check_major_ls_blueprint
    from functions.project_major_ls import project_major_ls_blueprint
    from functions.get_hide_tag import hide_tag_blueprint
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(blueprint=init_data_blueprint)
    app.register_blueprint(blueprint=login_blueprint)
    app.register_blueprint(blueprint=headquarter_blueprint)
    app.register_blueprint(blueprint=region_blueprint)
    app.register_blueprint(blueprint=project_blueprint)
    app.register_blueprint(blueprint=check_blueprint)
    app.register_blueprint(blueprint=analyze_blueprint)
    app.register_blueprint(blueprint=insight_blueprint)
    app.register_blueprint(blueprint=check_ls_blueprint)
    app.register_blueprint(blueprint=project_ls_blueprint)
    app.register_blueprint(blueprint=region_ls_blueprint)
    app.register_blueprint(blueprint=headquarter_ls_blueprint)
    app.register_blueprint(blueprint=insight_func_blueprint)
    app.register_blueprint(blueprint=province_info_blueprint)
    app.register_blueprint(blueprint=check_major_ls_blueprint)
    app.register_blueprint(blueprint=project_major_ls_blueprint)
    app.register_blueprint(blueprint=hide_tag_blueprint)
    # 这里调用前面定义的配置文件的对象
    app.config.from_object(config[config_name])
    # 初始化配置
    config[config_name].init_app(app)
    # 初始化数据库,官方定义.
    db.init_app(app)
    return app
