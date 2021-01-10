from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, session, json
from flask_sqlalchemy import SQLAlchemy

from functions.cache_data import *
init_data_blueprint = Blueprint('init_data', __name__, url_prefix='/init')


@init_data_blueprint.route('/get_all', methods=['GET', 'POST'])
def query_all():
    print("In func get all")
    return jsonify({"code": 0})





