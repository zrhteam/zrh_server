from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, session, json
import functions.cache_data as gl

from functions.cache_data import *
init_data_blueprint = Blueprint('init_data', __name__, url_prefix='/init')






