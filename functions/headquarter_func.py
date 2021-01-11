from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl

headquarter_blueprint = Blueprint('headquarter', __name__, url_prefix='/api/headquarter')

# # headquarter页面部分
# #
# # FunctionName: getRegionNumber
# # Purpose: 显示该公司(总部)有几个大区
# # Parameter:
# # Return:
# @headquarter_blueprint.route('/head_region', methods=['POST', 'GET'])
# def head_region():
#     print("In function get_region_number")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name " + str(headquarter_name))
#     resp_data = { "code": 10000, "data": {"region": []}}
#     cache_prj_with_tag = gl.get_value("cache_prj_with_tag")
#     for item in cache_prj_with_tag:
#         if headquarter_name == item.headquarter_tag:
#             resp_data["data"]["region"].append(item.region_tag)
#     if len(resp_data["data"]["region"]) == 0:
#         resp_data["code"] = -1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getCompanyDangerIndex
# Purpose: 显示整个公司检查后的总体危险指数以及各专业对应的危险指数
# Parameter:
# Return:


# headquarter页面部分
#
# FunctionName: getRectification
# Purpose: 获取公司项目整改率
# Parameter:
# Return:
@headquarter_blueprint.route('/head_rectification', methods=['POST', 'GET'])
def head_rectification():
    print("In function head_rectification")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = { "code": 10000, "data": {"rectification": "0%"}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    state_ok = 0
    state_nok = 0
    for item in cache_cascade_record:
        if headquarter_name == item.headquarter_tag:
            if item.state == 5:
                state_ok += 1
            else:
                state_nok += 1
    if state_ok + state_nok != 0:
        resp_data["data"]["rectification"] = str(round(state_ok * 100 / (state_ok + state_nok), 2)) + "%"
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadRiskLevel
# Purpose: 展示总部各风险等级及其对应的隐患数量
# Parameter:
# Return:
@headquarter_blueprint.route('/head_risk_level', methods=['POST', 'GET'])
def head_risk_level():
    print("In function head_risk_level")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = { "code": 10000, "data": {"risk_level": {"1": 0, "2": 0, "3": 0}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if headquarter_name == item.headquarter_tag:
            resp_data["data"]["risk_level"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadIndexRank
# Purpose: 根据风险指数对项目进行排序
# Parameter:
# Return:


# headquarter页面部分
#
# FunctionName: getHeadRiskRank
# Purpose: 显示根据高风险数量排名的项目名称
# Parameter:
# Return:
@headquarter_blueprint.route('/head_risk_rank', methods=['POST', 'GET'])
def head_risk_rank():
    print("In function head_risk_rank")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = { "code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    project_high_risk_map = {}
    for item in cache_cascade_record:
        if headquarter_name == item.headquarter_tag:
            if item.project_tag not in project_high_risk_map.keys():
                project_high_risk_map[item.project_tag] = 0
            if item.risk_level == "3":
                project_high_risk_map[item.project_tag] += 1
    res = sorted(project_high_risk_map.items(), key=lambda d: d[1], reverse=True)
    idx = 1
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "high_risk_count": ele[1]}
        idx += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getCompanyHighImage
# Purpose: 显示属于同一总部的未整改的高风险隐患图片
# Parameter:
# Return:
@headquarter_blueprint.route('/head_high_image', methods=['POST', 'GET'])
def head_high_image():
    print("In function head_high_image")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = { "code": 10000, "data": {"image_list": []}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    cache_sys_file = gl.get_value("cache_sys_file")
    image_id_list = {}
    for item in cache_cascade_record:
        if headquarter_name == item.headquarter_tag:
            if item.risk_level == "3" and item.state != "5":
                tmp_image_id_list = str(item.images_file_id).split(",")
                for ele in tmp_image_id_list:
                    image_id_list[ele] = 0
    for ele in cache_sys_file:
        if ele in image_id_list.keys():
            image_url = ele.upload_host + ele.directory + ele.name
            resp_data["data"]["image_list"].append(image_url)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)



# headquarter页面部分
#
# FunctionName: getCompanyRankTop
# Purpose: 显示隐患数量排名前10的隐患
# Parameter:
# Return:
@headquarter_blueprint.route('/head_rank_top', methods=['POST', 'GET'])
def head_rank_top():
    print("In function head_rank_top")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = { "code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    risk_note_map = {}
    for item in cache_cascade_record:
        if headquarter_name == item.headquarter_tag:
            if item.note not in risk_note_map.keys():
                risk_note_map[item.project_tag] = 0
            risk_note_map[item.note] += 1
    res = sorted(risk_note_map.items(), key=lambda d: d[1], reverse=True)
    idx = 1
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "count": ele[1]}
        idx += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadRiskList
# Purpose: 显示未整改高风险隐患列表
# Parameter:
# Return:
@headquarter_blueprint.route('/head_risk_list', methods=['POST', 'GET'])
def head_risk_list():
    print("In function head_risk_list")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {"note_list": []}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if headquarter_name == item.headquarter_tag:
            if item.risk_level == "3" and item.state != "5":
                resp_data["data"]["note_list"].append(item.note)


    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

