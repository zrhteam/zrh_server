from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl

region_blueprint = Blueprint('region', __name__, url_prefix='/api/region')


# region页面部分
#
# FunctionName: getRegionIndex
# Purpose: 显示该区域整体安全指数以及各专业安全指数
# Parameter:
# Return:

# region页面部分
#
# FunctionName: getRectificationNumber
# Purpose: 显示当前已检查项目数量
# Parameter:
# Return:
@region_blueprint.route('/region_project', methods=['POST'])
def region_project():
    print("In function get_region_number")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    cache_prj_with_tag = gl.get_value("cache_prj_with_tag")
    resp_data = { "code": 10000, "data": {"rectification_number": 0}}
    for item in cache_prj_with_tag:
        if region_name == item.region_tag:
            resp_data["data"]["rectification_number"] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionRiskLevel
# Purpose: 显示该区域各风险等级对应的隐患数量
# Parameter:
# Return:
@region_blueprint.route('/region_risk_level', methods=['POST', 'GET'])
def region_risk_level():
    print("In function region_risk_level")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = { "code": 10000, "data": {"risk_level": {"1": 0, "2": 0, "3": 0}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            resp_data["data"]["risk_level"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# region页面部分
#
# FunctionName: getRegionHighRIsk
# Purpose: 显示该区域未整改高风险隐患描述列表
# Parameter:
# Return:
@region_blueprint.route('/region_risk_list', methods=['POST', 'GET'])
def region_risk_list():
    print("In function region_risk_list")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = { "code": 10000, "data": {"note_list": []}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.risk_level == "3" and item.state != "5":
                resp_data["data"]["note_list"].append(item.note)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionHighImage
# Purpose: 显示该区域未整改高风险隐患图片
# Parameter:
# Return:
@region_blueprint.route('/region_high_image', methods=['POST', 'GET'])
def region_high_image():
    print("In function region_high_image")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = { "code": 10000, "data": {"image_list": []}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    cache_sys_file = gl.get_value("cache_sys_file")
    image_id_list = {}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.risk_level == "3" and item.state != "5":
                tmp_image_id_list = str(item.images_file_id).split(",")
                for ele in tmp_image_id_list:
                    image_id_list[ele] = 0
    for ele in cache_sys_file:
        if str(ele.id) in image_id_list.keys():
            image_url = ele.upload_host + ele.directory + ele.name
            resp_data["data"]["image_list"].append(image_url)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# region页面部分
#
# FunctionName: getRegionDistribution
# Purpose: 显示该区域各项目隐患数量在各风险等级和在各专业上的分布
# Parameter:
# Return:
@region_blueprint.route('/region_distribution', methods=['POST', 'GET'])
def region_distribution():
    print("In function region_distribution")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = { "code": 10000, "data": {"project_distribution": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.project_tag not in resp_data["data"]["project_distribution"].keys():
                resp_data["data"]["project_distribution"][item.project_tag] = {"risk_level": {"1": 0, "2": 0, "3": 0}, "major": {}}
            resp_data["data"]["project_distribution"][item.project_tag]["risk_level"][str(item.risk_level)] += 1
            if item.major_name not in resp_data["data"]["project_distribution"][item.project_tag]["major"].keys():
                resp_data["data"]["project_distribution"][item.project_tag]["major"][item.major_name] = 0
            resp_data["data"]["project_distribution"][item.project_tag]["major"][item.major_name] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionRankTop
# Purpose: 显示隐患数量排名前10的隐患描述
# Parameter:
# Return:
@region_blueprint.route('/region_rank_top', methods=['POST', 'GET'])
def region_rank_top():
    print("In function region_rank_top")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = { "code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    risk_note_map = {}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.note not in risk_note_map.keys():
                risk_note_map[item.note] = 0
            risk_note_map[item.note] += 1
    res = sorted(risk_note_map.items(), key=lambda d: d[1], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "count": ele[1]}
        idx += 1
        if idx == 10:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# region页面部分
#
# FunctionName: getRegionIndexRank
# Purpose: 显示按照安全指数排名后的项目名称
# Parameter:
# Return:


# region页面部分
#
# FunctionName: getRegionRiskNumber
# Purpose: 显示按照隐患数量排名后的项目名称
# Parameter:
# Return:
@region_blueprint.route('/region_index_rank', methods=['POST', 'GET'])
def region_index_rank():
    print("In function region_index_rank")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = { "code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    risk_project_map = {}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.project_tag not in risk_project_map.keys():
                risk_project_map[item.project_tag] = 0
            risk_project_map[item.project_tag] += 1
    res = sorted(risk_project_map.items(), key=lambda d: d[1], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "count": ele[1]}
        idx += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)
