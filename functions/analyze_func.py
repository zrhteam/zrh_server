from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl
import time
from ops import db
from models.user_grant_chart import UserGrantChart

analyze_blueprint = Blueprint('analyze', __name__, url_prefix='/api/analyze')


# 数据分析页面部分
#
# FunctionName: getCheckNumber
# Purpose: 两个对象之间检查次数的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_check_number', methods=['POST', 'GET'])
def analysis_check_number():
    print("In function analysis_check_number")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {"check_time": 0.0}, "object2": {"check_time": 0.0}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    record1_map = {}
    record2_map = {}
    if level == "headquarter":
        for item in cache_cascade_record:
            if item.headquarter_tag in object1_map.keys():
                if item.project_code not in record1_map.keys():
                    resp_data["data"]["object1"]["check_time"] += 1
                    record1_map[item.project_code] = 0
            if item.headquarter_tag in object2_map.keys():
                if item.project_code not in record2_map.keys():
                    resp_data["data"]["object2"]["check_time"] += 1
                    record2_map[item.project_code] = 0
    elif level == "region":
        for item in cache_cascade_record:
            if item.region_tag in object1_map.keys():
                if item.project_code not in record1_map.keys():
                    resp_data["data"]["object1"]["check_time"] += 1
                    record1_map[item.project_code] = 0
            if item.region_tag in object2_map.keys():
                if item.project_code not in record2_map.keys():
                    resp_data["data"]["object2"]["check_time"] += 1
                    record2_map[item.project_code] = 0
    elif level == "project":
        for item in cache_cascade_record:
            if item.project_tag in object1_map.keys():
                if item.project_code not in record1_map.keys():
                    resp_data["data"]["object1"]["check_time"] += 1
                    record1_map[item.project_code] = 0
            if item.project_tag in object2_map.keys():
                if item.project_code not in record2_map.keys():
                    resp_data["data"]["object2"]["check_time"] += 1
                    record2_map[item.project_code] = 0
    elif level == "check":
        for item in cache_cascade_record:
            if item.project_code in object1_map.keys():
                if item.project_code not in record1_map.keys():
                    resp_data["data"]["object1"]["check_time"] += 1
                    record1_map[item.project_code] = 0
            if item.project_code in object2_map.keys():
                if item.project_code not in record2_map.keys():
                    resp_data["data"]["object2"]["check_time"] += 1
                    record2_map[item.project_code] = 0
    resp_data["data"]["object1"]["check_time"] = round(resp_data["data"]["object1"]["check_time"] / len(object1_list),
                                                       2)
    resp_data["data"]["object2"]["check_time"] = round(resp_data["data"]["object2"]["check_time"] / len(object2_list),
                                                       2)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 数据分析页面部分
#
# FunctionName: getProjectNumber
# Purpose: 两个对象之间项目数量的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_project_number', methods=['POST', 'GET'])
def analysis_project_number():
    print("In function analysis_project_number")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {"project_num": 0.0}, "object2": {"project_num": 0.0}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    record1_map = {}
    record2_map = {}
    if level == "headquarter":
        for item in cache_cascade_record:
            if item.headquarter_tag in object1_map.keys():
                if item.project_tag not in record1_map.keys():
                    resp_data["data"]["object1"]["project_num"] += 1
                    record1_map[item.project_tag] = 0
            if item.headquarter_tag in object2_map.keys():
                if item.project_tag not in record2_map.keys():
                    resp_data["data"]["object2"]["project_num"] += 1
                    record2_map[item.project_tag] = 0
    elif level == "region":
        for item in cache_cascade_record:
            if item.region_tag in object1_map.keys():
                if item.project_tag not in record1_map.keys():
                    resp_data["data"]["object1"]["project_num"] += 1
                    record1_map[item.project_tag] = 0
            if item.region_tag in object2_map.keys():
                if item.project_tag not in record2_map.keys():
                    resp_data["data"]["object2"]["project_num"] += 1
                    record2_map[item.project_tag] = 0
    elif level == "project":
        for item in cache_cascade_record:
            if item.project_tag in object1_map.keys():
                if item.project_tag not in record1_map.keys():
                    resp_data["data"]["object1"]["project_num"] += 1
                    record1_map[item.project_tag] = 0
            if item.project_tag in object2_map.keys():
                if item.project_tag not in record2_map.keys():
                    resp_data["data"]["object2"]["project_num"] += 1
                    record2_map[item.project_tag] = 0
    elif level == "check":
        for item in cache_cascade_record:
            if item.project_tag in object1_map.keys():
                if item.project_tag not in record1_map.keys():
                    resp_data["data"]["object1"]["project_num"] += 1
                    record1_map[item.project_tag] = 0
            if item.project_tag in object2_map.keys():
                if item.project_tag not in record2_map.keys():
                    resp_data["data"]["object2"]["project_num"] += 1
                    record2_map[item.project_tag] = 0
    resp_data["data"]["object1"]["project_num"] = round(resp_data["data"]["object1"]["project_num"] / len(object1_list),
                                                        2)
    resp_data["data"]["object2"]["project_num"] = round(resp_data["data"]["object2"]["project_num"] / len(object2_list),
                                                        2)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 数据分析页面部分
#
# FunctionName: getMajorRiskNumber
# Purpose: 两个对象之间不同专业隐患数量的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_major_number', methods=['POST', 'GET'])
def analysis_major_number():
    print("In function analysis_major_number")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {}, "object2": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            if item.major_name not in resp_data["data"]["object1"].keys():
                resp_data["data"]["object1"] \
                    = {item.major_name: {"appear_time": 0, "system": {}}}
            if item.system_name not in resp_data["data"]["object1"][item.major_name]["system"].keys():
                resp_data["data"]["object1"][item.major_name]["system"] \
                    = {item.system_name: {"appear_time": 0, "equipment": {}}}
            if item.equipment_name not in resp_data["data"]["object1"][item.major_name]["system"][item.system_name][
                "equipment"].keys():
                resp_data["data"]["object1"][item.major_name]["system"][item.system_name]["equipment"] \
                    = {item.equipment_name: {"appear_time": 0, "module": {}}}
            if item.module_name not in \
                    resp_data["data"]["object1"][item.major_name]["system"][item.system_name]["equipment"][
                        item.equipment_name]["module"].keys():
                resp_data["data"]["object1"][item.major_name]["system"][item.system_name]["equipment"][
                    item.equipment_name]["module"] = {item.module_name: {"appear_time": 0}}
            resp_data["data"]["object1"][item.major_name]["appear_time"] += 1
            resp_data["data"]["object1"][item.major_name]["system"][item.system_name]["appear_time"] += 1
            resp_data["data"]["object1"][item.major_name]["system"][item.system_name]["equipment"][item.equipment_name][
                "appear_time"] += 1
            resp_data["data"]["object1"][item.major_name]["system"][item.system_name]["equipment"][item.equipment_name][
                "module"][item.module_name]["appear_time"] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            if item.major_name not in resp_data["data"]["object2"].keys():
                resp_data["data"]["object2"] \
                    = {item.major_name: {"appear_time": 0, "system": {}}}
            if item.system_name not in resp_data["data"]["object2"][item.major_name]["system"].keys():
                resp_data["data"]["object2"][item.major_name]["system"] \
                    = {item.system_name: {"appear_time": 0, "equipment": {}}}
            if item.equipment_name not in resp_data["data"]["object2"][item.major_name]["system"][item.system_name][
                "equipment"].keys():
                resp_data["data"]["object2"][item.major_name]["system"][item.system_name]["equipment"] \
                    = {item.equipment_name: {"appear_time": 0, "module": {}}}
            if item.module_name not in \
                    resp_data["data"]["object2"][item.major_name]["system"][item.system_name]["equipment"][
                        item.equipment_name]["module"].keys():
                resp_data["data"]["object2"][item.major_name]["system"][item.system_name]["equipment"][
                    item.equipment_name]["module"] = {item.module_name: {"appear_time": 0}}
            resp_data["data"]["object2"][item.major_name]["appear_time"] += 1
            resp_data["data"]["object2"][item.major_name]["system"][item.system_name]["appear_time"] += 1
            resp_data["data"]["object2"][item.major_name]["system"][item.system_name]["equipment"][
                item.equipment_name]["appear_time"] += 1
            resp_data["data"]["object2"][item.major_name]["system"][item.system_name]["equipment"][
                item.equipment_name]["module"][item.module_name]["appear_time"] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 数据分析页面部分
#
# FunctionName: getRiskLevel
# Purpose: 两个对象之间各风险等级隐患数量的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_risk_level', methods=['POST', 'GET'])
def analysis_risk_level():
    print("In function analysis_risk_level")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {"risk_level": {"1": 0, "2": 0, "3": 0}},
                                         "object2": {"risk_level": {"1": 0, "2": 0, "3": 0}}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            resp_data["data"]["object1"]["risk_level"][str(item.risk_level)] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            resp_data["data"]["object2"]["risk_level"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 数据分析页面部分
#
# FunctionName: getAreaRisk
# Purpose: 两个对象之间不同分布区域隐患数量的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_area_risk', methods=['POST', 'GET'])
def analysis_area_risk():
    print("In function analysis_area_risk")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {}, "object2": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            if item.area not in resp_data["data"]["object1"].keys():
                resp_data["data"]["object1"][item.area] = {"appear_time": 0}
            resp_data["data"]["object1"][item.area]["appear_time"] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            if item.area not in resp_data["data"]["object2"].keys():
                resp_data["data"]["object2"][item.area] = {"appear_time": 0}
            resp_data["data"]["object2"][item.area]["appear_time"] += 1
    res = sorted(resp_data["data"]["object1"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object1"] = {}
    for ele in res:
        resp_data["data"]["object1"][ele[0]] = ele[1]
        resp_data["data"]["object1"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    res = sorted(resp_data["data"]["object2"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object2"] = {}
    for ele in res:
        resp_data["data"]["object2"][ele[0]] = ele[1]
        resp_data["data"]["object2"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 数据分析页面部分
#
# FunctionName: getStageRisk
# Purpose: 两个对象之间不同致因阶段隐患数量的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_stage_risk', methods=['POST', 'GET'])
def analysis_stage_risk():
    print("In function analysis_stage_risk")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {}, "object2": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            if item.stage not in resp_data["data"]["object1"].keys():
                resp_data["data"]["object1"][item.stage] = {"appear_time": 0}
            resp_data["data"]["object1"][item.stage]["appear_time"] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            if item.stage not in resp_data["data"]["object2"].keys():
                resp_data["data"]["object2"][item.stage] = {"appear_time": 0}
            resp_data["data"]["object2"][item.stage]["appear_time"] += 1
    res = sorted(resp_data["data"]["object1"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object1"] = {}
    for ele in res:
        resp_data["data"]["object1"][ele[0]] = ele[1]
        resp_data["data"]["object1"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    res = sorted(resp_data["data"]["object2"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object2"] = {}
    for ele in res:
        resp_data["data"]["object2"][ele[0]] = ele[1]
        resp_data["data"]["object2"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 数据分析页面部分
#
# FunctionName: getTopNumber
# Purpose: 两个对象之间出现次数前top的隐患的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_top_number', methods=['POST', 'GET'])
def analysis_top_number():
    print("In function analysis_top_number")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {}, "object2": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            if item.note not in resp_data["data"]["object1"].keys():
                resp_data["data"]["object1"][item.note] = {"appear_time": 0}
            resp_data["data"]["object1"][item.note]["appear_time"] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            if item.note not in resp_data["data"]["object2"].keys():
                resp_data["data"]["object2"][item.note] = {"appear_time": 0}
            resp_data["data"]["object2"][item.note]["appear_time"] += 1
    res = sorted(resp_data["data"]["object1"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object1"] = {}
    for ele in res:
        resp_data["data"]["object1"][ele[0]] = ele[1]
        resp_data["data"]["object1"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    res = sorted(resp_data["data"]["object2"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object2"] = {}
    for ele in res:
        resp_data["data"]["object2"][ele[0]] = ele[1]
        resp_data["data"]["object2"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 数据分析页面部分
#
# FunctionName: getLawTop
# Purpose: 两个对象之间违反次数最多的法规标准的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_law_top', methods=['POST', 'GET'])
def analysis_law_top():
    print("In function analysis_law_top")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {}, "object2": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.rule_name is None:
            continue
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            if item.rule_name not in resp_data["data"]["object1"].keys():
                resp_data["data"]["object1"][item.rule_name] = {"appear_time": 0}
            resp_data["data"]["object1"][item.rule_name]["appear_time"] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            if item.rule_name not in resp_data["data"]["object2"].keys():
                resp_data["data"]["object2"][item.rule_name] = {"appear_time": 0}
            resp_data["data"]["object2"][item.rule_name]["appear_time"] += 1
    res = sorted(resp_data["data"]["object1"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object1"] = {}
    for ele in res:
        resp_data["data"]["object1"][ele[0]] = ele[1]
        resp_data["data"]["object1"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    res = sorted(resp_data["data"]["object2"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object2"] = {}
    for ele in res:
        resp_data["data"]["object2"][ele[0]] = ele[1]
        resp_data["data"]["object2"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 数据分析页面部分
#
# FunctionName: getModuleNumberTop
# Purpose: 两个对象之间出现隐患次数前top的组件的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_module_top', methods=['POST', 'GET'])
def analysis_module_top():
    print("In function analysis_module_top")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {}, "object2": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            if item.module_name not in resp_data["data"]["object1"].keys():
                resp_data["data"]["object1"][item.module_name] = {"appear_time": 0}
            resp_data["data"]["object1"][item.module_name]["appear_time"] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            if item.module_name not in resp_data["data"]["object2"].keys():
                resp_data["data"]["object2"][item.module_name] = {"appear_time": 0}
            resp_data["data"]["object2"][item.module_name]["appear_time"] += 1
    res = sorted(resp_data["data"]["object1"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object1"] = {}
    for ele in res:
        resp_data["data"]["object1"][ele[0]] = ele[1]
        resp_data["data"]["object1"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    res = sorted(resp_data["data"]["object2"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object2"] = {}
    for ele in res:
        resp_data["data"]["object2"][ele[0]] = ele[1]
        resp_data["data"]["object2"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 数据分析页面部分
#
# FunctionName: getEquipmentNumberTop
# Purpose: 两个对象之间出现隐患次数前top的设备的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_equipment_top', methods=['POST', 'GET'])
def analysis_equipment_top():
    print("In function analysis_equipment_top")
    start_t = datetime.now()
    # level = request.form.get("level")
    # object1 = request.form.get("object1")
    # object2 = request.form.get("object2")
    level = request.values.get("level")
    object1 = request.values.get("object1")
    object2 = request.values.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {}, "object2": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            if item.equipment_name not in resp_data["data"]["object1"].keys():
                resp_data["data"]["object1"][item.equipment_name] = {"appear_time": 0}
            resp_data["data"]["object1"][item.equipment_name]["appear_time"] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            if item.equipment_name not in resp_data["data"]["object2"].keys():
                resp_data["data"]["object2"][item.equipment_name] = {"appear_time": 0}
            resp_data["data"]["object2"][item.equipment_name]["appear_time"] += 1
    res = sorted(resp_data["data"]["object1"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    resp_data["data"]["object1"] = {}
    idx = 0
    for ele in res:
        resp_data["data"]["object1"][ele[0]] = ele[1]
        resp_data["data"]["object1"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    res = sorted(resp_data["data"]["object2"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object2"] = {}
    for ele in res:
        resp_data["data"]["object2"][ele[0]] = ele[1]
        resp_data["data"]["object2"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 数据分析页面部分
#
# FunctionName: getSystemNumberTop
# Purpose: 两个对象之间出现隐患次数前top的系统的对比
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_system_top', methods=['POST', 'GET'])
def analysis_system_top():
    print("In function analysis_system_top")
    start_t = datetime.now()
    level = request.form.get("level")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    object1_list = object1.split(",")
    object2_list = object2.split(",")
    object1_map = {}
    object2_map = {}
    for item in object1_list:
        object1_map[item] = 0
    for item in object2_list:
        object2_map[item] = 0
    print("Received level " + str(level))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    resp_data = {"code": 10000, "data": {"object1": {}, "object2": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if item.headquarter_tag in object1_map.keys() or item.region_tag in object1_map.keys() or item.project_tag in object1_map.keys() or item.project_code in object1_map.keys():
            if item.system_name not in resp_data["data"]["object1"].keys():
                resp_data["data"]["object1"][item.system_name] = {"appear_time": 0}
            resp_data["data"]["object1"][item.system_name]["appear_time"] += 1
        if item.headquarter_tag in object2_map.keys() or item.region_tag in object2_map.keys() or item.project_tag in object2_map.keys() or item.project_code in object2_map.keys():
            if item.system_name not in resp_data["data"]["object2"].keys():
                resp_data["data"]["object2"][item.system_name] = {"appear_time": 0}
            resp_data["data"]["object2"][item.system_name]["appear_time"] += 1
    res = sorted(resp_data["data"]["object1"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object1"] = {}
    for ele in res:
        resp_data["data"]["object1"][ele[0]] = ele[1]
        resp_data["data"]["object1"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    res = sorted(resp_data["data"]["object2"].items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    resp_data["data"]["object2"] = {}
    for ele in res:
        resp_data["data"]["object2"][ele[0]] = ele[1]
        resp_data["data"]["object2"][ele[0]]["rank"] = idx
        idx += 1
        if idx == 20:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 数据分析页面部分
#
# FunctionName:
# Purpose: 存入授权数据
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_grant_info', methods=['POST', 'GET'])
def analysis_grant_info():
    print("In function analysis_grant_info")
    start_t = datetime.now()
    level = request.form.get("level")
    title = request.form.get("title")
    object1 = request.form.get("object1")
    object2 = request.form.get("object2")
    user_name = request.form.get("user_name")
    print("Received level " + str(level))
    print("Received title " + str(title))
    print("Received object1 " + str(object1))
    print("Received object2 " + str(object2))
    print("Received user_name " + str(user_name))
    resp_data = {"code": 10000, "data": {"state": ""}}
    ugc = UserGrantChart(0, level, title, object1, object2, user_name)
    try:
        db.session.add(ugc)
        db.session.commit()
    except Exception as e:
        print("出现了 exception...")
        resp_data["data"]["state"] = "fail"
    else:
        resp_data["data"]["state"] = "success"
    finally:
        print("Returned data: ")
        print(resp_data)
        end_t = datetime.now()
        print("Query total time is: " + str((end_t - start_t).seconds) + "s")
        return jsonify(resp_data)


# 数据分析页面部分
#
# FunctionName:
# Purpose: 查询某个用户下授权的图
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_query_grant', methods=['POST', 'GET'])
def analysis_query_grant():
    print("In function analysis_query_grant")
    start_t = datetime.now()
    user_name = request.form.get("user_name")
    print("Received user_name " + str(user_name))
    resp_data = {"code": 10000, "data": []}
    charts = UserGrantChart.query.filter(user_name=user_name).all()
    for ele in charts:
        tmp_chart_map = {"level": ele.level, "title": ele.title, "object1": ele.object1, "object2": ele.object2}
        resp_data["data"].append(tmp_chart_map)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)



# 数据分析页面部分
#
# FunctionName:
# Purpose: 查询所有用户name
# Parameter:
# Return:
@analyze_blueprint.route('/analysis_all_user_name', methods=['POST', 'GET'])
def analysis_all_user_name():
    print("In function analysis_all_user_name")
    start_t = datetime.now()
    resp_data = {"code": 10000, "data": []}
    user_name = gl.get_value("cache_risk_user")
    for ele in user_name:
        resp_data["data"].append(ele.name)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)



