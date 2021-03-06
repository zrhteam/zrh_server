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
# @headquarter_blueprint.route('/head_rectification', methods=['POST', 'GET'])
# def head_rectification():
#     print("In function head_rectification")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {"rectification": "0%"}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     state_ok = 0
#     state_nok = 0
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             if item.state == 5:
#                 state_ok += 1
#             else:
#                 state_nok += 1
#     if state_ok + state_nok != 0:
#         resp_data["data"]["rectification"] = str(round(state_ok * 100 / (state_ok + state_nok), 2)) + "%"
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_rectification', methods=['POST', 'GET'])
def head_rectification():
    print("In function head_rectification")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {"rectification": "0%"}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    state_ok = 0
    state_nok = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
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
# FunctionName: getInitHeadRiskLevel
# Purpose: 展示总部各风险等级及其对应的隐患数量
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_risk_level', methods=['POST', 'GET'])
# def head_risk_level():
#     print("In function head_risk_level")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {"risk_level": {"1": 0, "2": 0, "3": 0}}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             resp_data["data"]["risk_level"][str(item.risk_level)] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_risk_level', methods=['POST', 'GET'])
def head_risk_level():
    print("In function head_risk_level")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {"risk_level": {"1": 0, "2": 0, "3": 0}}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
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
# Purpose: 显示每个区域的高风险数量
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_risk_rank', methods=['POST', 'GET'])
# def head_risk_rank():
#     print("In function head_risk_rank")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     region_high_risk_map = {}
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             region_name = item.region_tag if item.region_tag is not None else "空"
#             if region_name not in region_high_risk_map.keys():
#                 region_high_risk_map[region_name] = 0
#             if item.risk_level == "3":
#                 region_high_risk_map[region_name] += 1
#     res = sorted(region_high_risk_map.items(), key=lambda d: d[1], reverse=True)
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = {"rank": idx, "high_risk_count": ele[1]}
#         idx += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     print(resp_data)
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_risk_rank', methods=['POST', 'GET'])
def head_risk_rank():
    print("In function head_risk_rank")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = {"project_tag": item.project_tag, "region_tag": item.region_tag, "headquarter_tag": item.headquarter_tag}
    region_high_risk_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            region_name = contained_check_map[item.project_code]["region_tag"] if contained_check_map[item.project_code]["region_tag"] is not None else "空"
            if region_name not in region_high_risk_map.keys():
                region_high_risk_map[region_name] = 0
            if item.risk_level == "3":
                region_high_risk_map[region_name] += 1
    res = sorted(region_high_risk_map.items(), key=lambda d: d[1], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "high_risk_count": ele[1]}
        idx += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    print(resp_data)
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getCompanyHighImage
# Purpose: 显示属于同一总部的未整改的高风险隐患图片 以及隐患描述
# Parameter:
# Return:
# 修改前： {"data": {"image_list": [url1, url2, ...]}}
# 修改后： {"data": {"image_list": [{"url": url1, "note": note1}, {"url": url1, "note": note1}, ...]}}
# @headquarter_blueprint.route('/head_high_image', methods=['POST', 'GET'])
# def head_high_image():
#     print("In function head_high_image")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {"image_list": []}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     cache_sys_file = gl.get_value("cache_sys_file")
#     image_id_list = {}
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             if item.risk_level == "3" and item.state != "5":
#                 tmp_image_id_list = str(item.images_file_id).split(",")
#                 for ele in tmp_image_id_list:
#                     # image_id_list[ele] = 0
#                     image_id_list[ele] = {"note": item.note, "check_name": item.project_name}
#     for ele in cache_sys_file:
#         if str(ele.id) in image_id_list.keys():
#             image_url = ele.upload_host + ele.directory + ele.name
#             resp_data["data"]["image_list"].append({"image_url": image_url, "check_name": image_id_list[str(ele.id)]["check_name"],
#                                                     "note": image_id_list[str(ele.id)]["note"]})
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_high_image', methods=['POST', 'GET'])
def head_high_image():
    print("In function head_high_image")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {"image_list": []}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    cache_sys_file = gl.get_value("sys_file")
    image_id_list = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.risk_level == "3" and item.state != "5":
                tmp_image_id_list = str(item.images_file_id).split(",")
                for ele in tmp_image_id_list:
                    # image_id_list[ele] = 0
                    image_id_list[ele] = {"note": item.note, "check_name": item.project_name}
    for ele in cache_sys_file:
        if str(ele.id) in image_id_list.keys():
            image_url = ele.upload_host + ele.directory + ele.name
            resp_data["data"]["image_list"].append({"image_url": image_url, "check_name": image_id_list[str(ele.id)]["check_name"],
                                                    "note": image_id_list[str(ele.id)]["note"]})
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# # headquarter页面部分
# #
# # FunctionName: getCompanyHighImage
# # Purpose: 显示属于同一总部的未整改的高风险隐患图片 以及隐患描述
# # Parameter:
# # Return:
# @headquarter_blueprint.route('/head_high_image', methods=['POST', 'GET'])
# def head_high_image():
#     print("In function head_high_image")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     # top = int(request.form.get("top"))
#     print("Received headquarter_name " + str(headquarter_name))
#     # print("Received top " + str(top))
#     resp_data = {"code": 10000, "data": {"image_list": []}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     cache_sys_file = gl.get_value("cache_sys_file")
#     image_id_list = {}
#     # resp_data["check_code"] = latest_map["check_code"]
#     # resp_data["check_time"] = latest_map["time"]
#     for item in cache_cascade_record:
#         if headquarter_name == item.region_tag:
#             tmp_image_id_list = str(item.images_file_id).split(",")
#             for ele in tmp_image_id_list:
#                 image_id_list[ele] = {}
#                 image_id_list[ele]["check_name"] = item.project_name
#                 image_id_list[ele]["note"] = item.note
#                 print("debug..." + str(item.create_time))
#                 image_id_list[ele]["create_time"] = int(time.mktime(time.strptime(str(item.create_time), "%Y-%m-%d %H:%M:%S")))
#     res = sorted(image_id_list.items(), key=lambda d: d[1]["create_time"], reverse=True)
#     image_id_list = {}
#     idx = 0
#     # 取出前10张
#     for ele in res:
#         image_id_list[ele[0]] = ele[1]
#         idx += 1
#         if idx == 10:
#             break
#     for ele in cache_sys_file:
#         if str(ele.id) in image_id_list.keys():
#             image_url = ele.upload_host + ele.directory + ele.name
#             resp_data["data"]["image_list"].append({"image_url": image_url, "check_name": image_id_list[str(ele.id)]["check_name"], "note": image_id_list[str(ele.id)]["note"]})
#     # # 取前10张
#     # resp_data["data"]["image_list"] = resp_data["data"]["image_list"][0: 10]
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getInitNumberTop
# Purpose: 显示隐患数量排名前10的隐患
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_rank_top', methods=['POST', 'GET'])
# def head_rank_top():
#     print("In function head_rank_top")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     condition = request.form.get("condition")
#     top = int(request.form.get("top"))
#     print("Received headquarter_name " + str(headquarter_name))
#     print("Received condition " + str(condition))
#     print("Received top " + str(top))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     risk_note_map = {}
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             if item.note not in risk_note_map.keys():
#                 if condition == "major":
#                     risk_note_map[item.note] = {"appear_time": 0, condition: item.major_name}
#                 elif condition == "system":
#                     risk_note_map[item.note] = {"appear_time": 0, condition: item.system_name}
#             risk_note_map[item.note]["appear_time"] += 1
#     res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = {"rank": idx, "count": ele[1]}
#         idx += 1
#         if idx == top:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_rank_top', methods=['POST', 'GET'])
def head_rank_top():
    print("In function head_rank_top")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    condition = request.form.get("condition")
    top = int(request.form.get("top"))
    print("Received headquarter_name " + str(headquarter_name))
    print("Received condition " + str(condition))
    print("Received top " + str(top))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    risk_note_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.note not in risk_note_map.keys():
                if condition == "major":
                    risk_note_map[item.note] = {"appear_time": 0, condition: item.major_name}
                elif condition == "system":
                    risk_note_map[item.note] = {"appear_time": 0, condition: item.system_name}
            risk_note_map[item.note]["appear_time"] += 1
    res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "count": ele[1]}
        idx += 1
        if idx == top:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadRiskLevelYear
# Purpose: 按年份显示总部的高中低风险等级对应的隐患数量
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_risk_level_year', methods=['POST', 'GET'])
# def head_risk_level_year():
#     print("In function head_risk_level_year")
#     start_t = datetime.now()
#     # headquarter_name = request.form.get("headquarter_name")
#     headquarter_name = request.values.get("headquarter_name")
#     print("Received headquarter_name: " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             cur_year = str(item.create_time).split('-')[0]
#             if cur_year not in resp_data["data"].keys():
#                 resp_data["data"][cur_year] = {"1": 0, "2": 0, "3": 0}
#             resp_data["data"][cur_year][item.risk_level] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_risk_level_year', methods=['POST', 'GET'])
def head_risk_level_year():
    print("In function head_risk_level_year")
    start_t = datetime.now()
    # headquarter_name = request.form.get("headquarter_name")
    headquarter_name = request.values.get("headquarter_name")
    print("Received headquarter_name: " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            cur_year = str(item.create_time).split('-')[0]
            if cur_year not in resp_data["data"].keys():
                resp_data["data"][cur_year] = {"1": 0, "2": 0, "3": 0}
            resp_data["data"][cur_year][item.risk_level] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadOtherNumberTop
# Purpose: 显示在不同条件（风险等级(1, 2,3, all)/致因阶段/分布区域）下，出现次数排名前top的隐患描述
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_risk_other_top', methods=['POST', 'GET'])
# def head_risk_other_top():
#     print("In function head_risk_other_top")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     flag = int(request.form.get("flag"))
#     top = int(request.form.get("top"))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     if flag == 1:  # 致因阶段
#         stage = request.form.get("stage")
#         print("Received stage " + str(stage))
#         for item in cache_cascade_record:
#             t_stage = ''
#             if item.stage == '':
#                 t_stage = "未定义"
#             else:
#                 t_stage = item.stage.split("阶段")[0]
#             if headquarter_name == item.headquarter_tag and t_stage == stage:
#                 if item.note not in resp_data["data"].keys():
#                     resp_data["data"][item.note] = 0
#                 resp_data["data"][item.note] += 1
#     elif flag == 2:  # 风险等级
#         risk_level = request.form.get("risk_level")
#         print("Received risk_level " + str(risk_level))
#         for item in cache_cascade_record:
#             if headquarter_name == item.headquarter_tag:
#                 if risk_level == "all" or risk_level == item.risk_level:
#                     if item.note not in resp_data["data"].keys():
#                         resp_data["data"][item.note] = 0
#                     resp_data["data"][item.note] += 1
#     elif flag == 3:  # 专业
#         major_name = request.form.get("major_name")
#         print("Received major_name " + str(major_name))
#         for item in cache_cascade_record:
#             if headquarter_name == item.headquarter_tag and major_name == item.major_name:
#                 if item.note not in resp_data["data"].keys():
#                     resp_data["data"][item.note] = 0
#                 resp_data["data"][item.note] += 1
#     elif flag == 4:  # 专业 + 系统
#         major_name = request.form.get("major_name")
#         system_name = request.form.get("system_name")
#         print("Received major_name " + str(major_name))
#         print("Received system_name " + str(system_name))
#         for item in cache_cascade_record:
#             if headquarter_name == item.headquarter_tag and major_name == item.major_name and system_name == item.system_name:
#                 if item.note not in resp_data["data"].keys():
#                     resp_data["data"][item.note] = 0
#                 resp_data["data"][item.note] += 1
#     elif flag == 5:  # 专业 + 区域
#         major_name = request.form.get("major_name")
#         area = request.form.get("area")
#         print("Received major_name " + str(major_name))
#         print("Received area " + str(area))
#         for item in cache_cascade_record:
#             if headquarter_name == item.headquarter_tag and major_name == item.major_name and area == item.area:
#                 if item.note not in resp_data["data"].keys():
#                     resp_data["data"][item.note] = 0
#                 resp_data["data"][item.note] += 1
#
#     res = sorted(resp_data["data"].items(), key=lambda d: d[1], reverse=True)
#     resp_data["data"] = {}
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = ele[1]
#         idx += 1
#         if idx == top:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_risk_other_top', methods=['POST', 'GET'])
def head_risk_other_top():
    print("In function head_risk_other_top")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    flag = int(request.form.get("flag"))
    top = int(request.form.get("top"))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    if flag == 1:  # 致因阶段
        stage = request.form.get("stage")
        print("Received stage " + str(stage))
        cache_final_tag = gl.get_value("final_tag")
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            t_stage = ''
            if item.stage == '':
                t_stage = "未定义"
            else:
                t_stage = item.stage.split("阶段")[0]
            if item.project_code in contained_check_map.keys() and t_stage == stage:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1
    elif flag == 2:  # 风险等级
        risk_level = request.form.get("risk_level")
        print("Received risk_level " + str(risk_level))
        cache_final_tag = gl.get_value("final_tag")
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys():
                if risk_level == "all" or risk_level == item.risk_level:
                    if item.note not in resp_data["data"].keys():
                        resp_data["data"][item.note] = 0
                    resp_data["data"][item.note] += 1
    elif flag == 3:  # 专业
        major_name = request.form.get("major_name")
        print("Received major_name " + str(major_name))
        cache_final_tag = gl.get_value("final_tag")
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys() and major_name == item.major_name:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1
    elif flag == 4:  # 专业 + 系统
        major_name = request.form.get("major_name")
        system_name = request.form.get("system_name")
        print("Received major_name " + str(major_name))
        print("Received system_name " + str(system_name))
        cache_final_tag = gl.get_value("final_tag")
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys() and major_name == item.major_name and system_name == item.system_name:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1
    elif flag == 5:  # 专业 + 区域
        major_name = request.form.get("major_name")
        area = request.form.get("area")
        print("Received major_name " + str(major_name))
        print("Received area " + str(area))
        cache_final_tag = gl.get_value("final_tag")
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys() and major_name == item.major_name and area == item.area:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1

    res = sorted(resp_data["data"].items(), key=lambda d: d[1], reverse=True)
    resp_data["data"] = {}
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = ele[1]
        idx += 1
        if idx == top:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadCheckRank
# Purpose: 按照检查次数对区域排名
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_check_rank', methods=['POST', 'GET'])
# def head_check_rank():
#     print("In function head_check_rank")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name: " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     risk_check_map = {}
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             if item.project_name not in risk_check_map.keys():
#                 risk_check_map[item.project_name] = 0
#                 if item.region_tag not in resp_data["data"].keys():
#                     resp_data["data"][item.region_tag] = 0
#                 resp_data["data"][item.region_tag] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_check_rank', methods=['POST', 'GET'])
def head_check_rank():
    print("In function head_check_rank")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name: " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = {"project_tag": item.project_tag, "region_tag": item.region_tag, "headquarter_tag": item.headquarter_tag}
    risk_check_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.project_name not in risk_check_map.keys():
                risk_check_map[item.project_name] = 0
                if contained_check_map[item.project_code]["region_tag"] not in resp_data["data"].keys():
                    resp_data["data"][contained_check_map[item.project_code]["region_tag"]] = 0
                resp_data["data"][contained_check_map[item.project_code]["region_tag"]] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadMajorRatio
# Purpose:各专业隐患数量占比
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_major_ratio', methods=['POST', 'GET'])
# def head_major_ratio():
#     print("In function head_major_ratio")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name: " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             # cur_year = str(item.create_time).split('-')[0]
#             if item.major_name not in resp_data["data"].keys():
#                 resp_data["data"][item.major_name] = 0
#             resp_data["data"][item.major_name] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_major_ratio', methods=['POST', 'GET'])
def head_major_ratio():
    print("In function head_major_ratio")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name: " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            # cur_year = str(item.create_time).split('-')[0]
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = 0
            resp_data["data"][item.major_name] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadStageRatio
# Purpose: 各致因阶段的隐患数量占比情况
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_stage_ratio', methods=['POST', 'GET'])
# def head_stage_ratio():
#     print("In function head_stage_ratio")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name " + str(headquarter_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             stage = ''
#             if item.stage == '':
#                 stage = "未定义"
#             else:
#                 stage = item.stage.split("阶段")[0]
#             # stage = "not defined stage" if item.stage == '' else item.stage
#             # if
#             if item.major_name not in resp_data["data"].keys():
#                 resp_data["data"][item.major_name] = {}
#             if stage not in resp_data["data"][item.major_name].keys():
#                 resp_data["data"][item.major_name][stage] = 0
#             resp_data["data"][item.major_name][stage] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_stage_ratio', methods=['POST', 'GET'])
def head_stage_ratio():
    print("In function head_stage_ratio")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            stage = ''
            if item.stage == '':
                stage = "未定义"
            else:
                stage = item.stage.split("阶段")[0]
            # stage = "not defined stage" if item.stage == '' else item.stage
            # if
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = {}
            if stage not in resp_data["data"][item.major_name].keys():
                resp_data["data"][item.major_name][stage] = 0
            resp_data["data"][item.major_name][stage] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadAreaRatio
# Purpose: 根据隐患数量显示不同分布区域的占比情况
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_area_ratio', methods=['POST', 'GET'])
# def head_area_ratio():
#     print("In function head_area_ratio")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     major = request.form.get("major")
#     print("Received headquarter_name " + str(headquarter_name))
#     print("Received major" + str(major))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             if major == item.major_name or major == "all":
#                 area = "未定义" if item.area == '' else item.area
#                 if item.major_name not in resp_data["data"].keys():
#                     resp_data["data"][item.major_name] = {}
#                 if area not in resp_data["data"][item.major_name].keys():
#                     resp_data["data"][item.major_name][area] = 0
#                 resp_data["data"][item.major_name][area] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_area_ratio', methods=['POST', 'GET'])
def head_area_ratio():
    print("In function head_area_ratio")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    major = request.form.get("major")
    print("Received headquarter_name " + str(headquarter_name))
    print("Received major" + str(major))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if major == item.major_name or major == "all":
                area = "未定义" if item.area == '' else item.area
                if item.major_name not in resp_data["data"].keys():
                    resp_data["data"][item.major_name] = {}
                if area not in resp_data["data"][item.major_name].keys():
                    resp_data["data"][item.major_name][area] = 0
                resp_data["data"][item.major_name][area] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadProjectRank
# Purpose: 按照项目数量对区域排名
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_region_rank', methods=['POST', 'GET'])
# def head_region_rank():
#     print("In function head_region_rank")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name: " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     risk_project_map = {}
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             if item.project_tag not in risk_project_map.keys():
#                 risk_project_map[item.project_tag] = 0
#                 if item.region_tag not in resp_data["data"].keys():
#                     resp_data["data"][item.region_tag] = 0
#                 resp_data["data"][item.region_tag] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_region_rank', methods=['POST', 'GET'])
def head_region_rank():
    print("In function head_region_rank")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name: " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = {"project_tag": item.project_tag, "region_tag": item.region_tag, "headquarter_tag": item.headquarter_tag}
    risk_project_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if contained_check_map[item.project_code]["project_tag"] not in risk_project_map.keys():
                risk_project_map[contained_check_map[item.project_code]["project_tag"]] = 0
                if contained_check_map[item.project_code]["region_tag"] not in resp_data["data"].keys():
                    resp_data["data"][contained_check_map[item.project_code]["region_tag"]] = 0
                resp_data["data"][contained_check_map[item.project_code]["region_tag"]] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadDangerProblem
# Purpose: 显示该总部存在的红线问题及其对应的原因
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_danger_problem', methods=['POST', 'GET'])
# def head_danger_problem():
#     print("In function head_danger_problem")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name: " + str(headquarter_name))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             if item.alert_indicator is not None:
#                 if item.alert_indicator not in resp_data["data"].keys():
#                     resp_data["data"][item.alert_indicator] = {"appear_time": 0, "problem": {}}
#                 resp_data["data"][item.alert_indicator]["appear_time"] += 1
#                 if item.problem1 is not None:
#                     if item.problem1 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem1] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem1]["appear_time"] += 1
#                 if item.problem2 is not None:
#                     if item.problem2 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem2] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem2]["appear_time"] += 1
#                 if item.problem3 is not None:
#                     if item.problem3 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem3] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem3]["appear_time"] += 1
#                 if item.problem4 is not None:
#                     if item.problem4 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem4] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem4]["appear_time"] += 1
#                 if item.problem5 is not None:
#                     if item.problem5 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem5] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem5]["appear_time"] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_danger_problem', methods=['POST', 'GET'])
def head_danger_problem():
    print("In function head_danger_problem")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name: " + str(headquarter_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.alert_indicator is not None:
                if item.alert_indicator not in resp_data["data"].keys():
                    resp_data["data"][item.alert_indicator] = {"appear_time": 0, "problem": {}}
                resp_data["data"][item.alert_indicator]["appear_time"] += 1
                if item.problem1 is not None:
                    if item.problem1 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem1] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem1]["appear_time"] += 1
                if item.problem2 is not None:
                    if item.problem2 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem2] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem2]["appear_time"] += 1
                if item.problem3 is not None:
                    if item.problem3 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem3] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem3]["appear_time"] += 1
                if item.problem4 is not None:
                    if item.problem4 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem4] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem4]["appear_time"] += 1
                if item.problem5 is not None:
                    if item.problem5 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem5] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem5]["appear_time"] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getDangerSelection
# Purpose: 返回专业、风险等级、致因阶段、分布区域的级联关系（major、risk_level、stage、area）
# Parameter:
# Return:
# @headquarter_blueprint.route('/danger_selection', methods=['POST', 'GET'])
# def danger_selection():
#     print("In function danger_selection")
#     start_t = datetime.now()
#     resp_data = {"code": 10000, "data": {"stage": [], "risk_level": ["1", "2", "3"],
#                                          "major_name": {}}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         stage = ''
#         if item.stage == '':
#             stage = "未定义"
#         else:
#             stage = item.stage.split("阶段")[0]
#         if stage not in resp_data["data"]["stage"]:
#             resp_data["data"]["stage"].append(stage)
#         if item.major_name not in resp_data["data"]["major_name"].keys():
#             resp_data["data"]["major_name"][item.major_name] = {"system_name": [], "area": []}
#         if item.system_name not in resp_data["data"]["major_name"][item.major_name]["system_name"]:
#             resp_data["data"]["major_name"][item.major_name]["system_name"].append(item.system_name)
#         if item.area not in resp_data["data"]["major_name"][item.major_name]["area"]:
#             resp_data["data"]["major_name"][item.major_name]["area"].append(item.area)
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/danger_selection', methods=['POST', 'GET'])
def danger_selection():
    print("In function danger_selection")
    start_t = datetime.now()
    resp_data = {"code": 10000, "data": {"stage": [], "risk_level": ["1", "2", "3"],
                                         "major_name": {}}}
    cache_cascade_record = gl.get_value("final_record")
    for item in cache_cascade_record:
        stage = ''
        if item.stage == '':
            stage = "未定义"
        else:
            stage = item.stage.split("阶段")[0]
        if stage not in resp_data["data"]["stage"]:
            resp_data["data"]["stage"].append(stage)
        if item.major_name not in resp_data["data"]["major_name"].keys():
            resp_data["data"]["major_name"][item.major_name] = {"system_name": [], "area": []}
        if item.system_name not in resp_data["data"]["major_name"][item.major_name]["system_name"]:
            resp_data["data"]["major_name"][item.major_name]["system_name"].append(item.system_name)
        if item.area not in resp_data["data"]["major_name"][item.major_name]["area"]:
            resp_data["data"]["major_name"][item.major_name]["area"].append(item.area)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# headquarter页面部分
#
# FunctionName: getHeadRiskLevelRatio
# Purpose: 不同专业下风险等级占比
# Parameter:
# Return:
# @headquarter_blueprint.route('/head_risk_level_ratio', methods=['POST', 'GET'])
# def head_risk_level_ratio():
#     print("In function head_risk_level_ratio")
#     start_t = datetime.now()
#     headquarter_name = request.form.get("headquarter_name")
#     print("Received headquarter_name " + str(headquarter_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     for item in cache_cascade_record:
#         if headquarter_name == item.headquarter_tag:
#             if item.major_name not in resp_data["data"].keys():
#                 resp_data["data"][item.major_name] = {}
#             if item.risk_level not in resp_data["data"][item.major_name].keys():
#                 resp_data["data"][item.major_name][item.risk_level] = 0
#             resp_data["data"][item.major_name][item.risk_level] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@headquarter_blueprint.route('/head_risk_level_ratio', methods=['POST', 'GET'])
def head_risk_level_ratio():
    print("In function head_risk_level_ratio")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = {}
            if item.risk_level not in resp_data["data"][item.major_name].keys():
                resp_data["data"][item.major_name][item.risk_level] = 0
            resp_data["data"][item.major_name][item.risk_level] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 所属项目名，对应的经纬度
@headquarter_blueprint.route('/head_project_position', methods=['POST', 'GET'])
def head_project_position():
    print("In function head_project_position")
    start_t = datetime.now()
    headquarter_name = request.form.get("headquarter_name")
    print("Received headquarter_name " + str(headquarter_name))
    cache_final_tag = gl.get_value("final_tag")
    cache_risk_project = gl.get_value("risk_project")
    contained_check_and_project_map = {}
    resp_data = {"code": 10000, "data": {}}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            if item.project_tag not in resp_data["data"].keys() and item.project_tag is not None:
                resp_data["data"][item.project_tag] = {"lat": "", "lng": ""}
            if item.code is not None and item.project_tag is not None:
                contained_check_and_project_map[item.code] = item.project_tag
    for item in cache_risk_project:
        if item.code in contained_check_and_project_map.keys():
            if item.lat is not None and item.lng is not None:
                resp_data["data"][contained_check_and_project_map[item.code]] = {"lat": str(item.lat), "lng": str(item.lng)}
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)