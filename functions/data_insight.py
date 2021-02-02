from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl
import time
from functions.file_reader import get_scatter, get_trend, get_correlation, get_change_point_and_outlier, \
    get_attribution, get_top10

insight_blueprint = Blueprint('insight', __name__, url_prefix='/api/analyze/insight')


# Analyze相关页面
#
# FunctionName: analyzeGetMainChartData
# Purpose: 获取Insight用于渲染散点图
# Parameter: None
# Return: json -> list of (pid, x, y, type)
@insight_blueprint.route('/main', methods=['POST'])
def analyze_get_main_chart_data():
    print("In function analyze_get_main_chart_data")
    start_t = datetime.now()

    # insight_list = [(1, 1, 2, 'top1'), (2, 3, 4, 'trend'), (3, 4, 5, 'correlation')]
    insight_list = get_scatter()

    insight_list = list(filter(lambda insight: all((str(attr) != 'nan') for attr in insight), insight_list))

    print("Returned result:")
    print(insight_list)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(insight_list)


# FunctionName: analyzeGetRefChartData
# Purpose: 获取Insight点击后出现的小图的数据
# Parameter: pid: insight的id, type: insight的种类
# Return: json
@insight_blueprint.route('/ref', methods=['POST'])
def analyze_get_ref_chart_data():
    print("In function analyze_get_ref_chart_data")
    pid = int(request.form.get("pid"))
    print("Received pid: " + str(pid))
    type_ = request.form.get("type")
    print("Received type: " + str(type_))
    start_t = datetime.now()

    res = {}

    if type_ == 'top1':
        y_coord_str, data_list = get_top10(pid)
        res['y_coord_str'] = y_coord_str
        res['data_list'] = [int(num) for num in data_list]

    elif type_ == 'trend':
        x_coord_str, y_coord_str, x_label_list, data_list = get_trend(pid)
        res['x_coord_str'] = x_coord_str
        res['y_coord_str'] = y_coord_str
        res['x_label_list'] = x_label_list
        res['data_list'] = [int(num) for num in data_list]

    elif type_ == 'correlation':
        x_coord_str, x_label_list, data_list = get_correlation(pid)
        res['x_coord_str'] = x_coord_str
        for item in data_list:
            item['list'] = [int(x) for x in item['list']]
        res['x_label_list'] = x_label_list
        res['data_list'] = data_list

    elif type_ == 'change point' or type_ == 'outlier':
        x_coord_str, y_coord_str, x_label_list, data_list, highlight_idx = get_change_point_and_outlier(pid)
        res['x_coord_str'] = x_coord_str
        res['y_coord_str'] = y_coord_str
        res['x_label_list'] = x_label_list
        res['data_list'] = [int(num) for num in data_list]
        res['highlight_idx'] = highlight_idx

    elif type_ == 'attribution':
        name_list, value_list = get_attribution(pid)
        data_list = [(str(name), int(value)) for name, value in zip(name_list, value_list)]
        res['data_list'] = data_list

    else:
        print(f'Type Error: {type_}')

    print("Returned result:")
    print(res)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(res)
