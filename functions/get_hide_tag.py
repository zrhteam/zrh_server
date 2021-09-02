from datetime import datetime

from flask import Blueprint, jsonify, request

import functions.cache_data as gl

hide_tag_blueprint = Blueprint('hide_tag', __name__, url_prefix='/api/analyze/hide_tag')


# 数据可视化系统脱敏
@hide_tag_blueprint.route('/get_hide_tag', methods=['POST', 'GET'])
def get_hide_tag():
    print("In function get_hide_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_head_map = {}
    head_hide_tag_map = {}
    region_hide_tag_map = {}
    project_hide_tag_map = {}
    resp_data = []
    # 首先筛选所有总部
    for item in cache_final_tag:
        if item.headquarter_tag is not None and str(item.headquarter_tag) not in contain_head_map.keys():
            contain_head_map[str(item.headquarter_tag)] = {}
            if item.headquarter_tag not in head_hide_tag_map.keys():
                if item.headquarter_hide_tag is not None:
                    head_hide_tag_map[str(item.headquarter_tag)] = str(item.headquarter_hide_tag)
                else:
                    head_hide_tag_map[str(item.headquarter_tag)] = str(item.headquarter_tag)

    # 再筛选所有区域
    for item in cache_final_tag:
        if item.headquarter_tag is not None and str(item.region_tag) not in contain_head_map[str(item.headquarter_tag)].keys():
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
            if str(item.headquarter_tag) + '/' + str(item.region_tag) not in region_hide_tag_map.keys():
                if item.region_hide_tag is not None:
                    region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = str(
                        item.region_hide_tag)
                else:
                    region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = str(item.region_tag)

    # 再筛选所有项目
    for item in cache_final_tag:
        if item.project_tag is not None and item.headquarter_tag is not None:
            if str(item.project_tag) not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
                if str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(
                        item.project_tag) not in project_hide_tag_map.keys():
                    if item.project_hide_tag is not None:
                        project_hide_tag_map[
                            str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(item.project_tag)] = \
                            str(item.project_hide_tag)
                    else:
                        project_hide_tag_map[
                            str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(item.project_tag)] = \
                            str(item.project_tag)
    # 筛选所有检查
    for item in cache_final_tag:
        if item.headquarter_tag is not None and item.project_tag is not None:
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)

    # 将返回数据格式化
    count = 0
    for head in contain_head_map:
        region_list = []
        for region in contain_head_map[head]:
            if region != 'None':
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"level": 4, "label": check_code, "value": check_code, "id": count})
                        count += 1
                    project_list.append(
                        {"level": 3, "label": project_hide_tag_map[head + '/' + region + '/' + project],
                         "value": project, "children": check_code_list, "id": count})
                    count += 1
                region_list.append(
                    {"level": 2, "label": region_hide_tag_map[head + '/' + region], "value": region,
                     "children": project_list, "id": count})
                count += 1
            else:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"level": 4, "label": check_code, "value": check_code, "id": count})
                        count += 1
                    project_list.append(
                        {"level": 3, "label": project_hide_tag_map[head + '/' + region + '/' + project],
                         "value": project, "children": check_code_list, "id": count})
                    count += 1
                region_list = project_list
        resp_data.append({"level": 1, "label": head_hide_tag_map[head], "value": head, "children": region_list, "id": count})
        count += 1
    print(resp_data)
    return jsonify(resp_data)


# 返回层级查询信息
@hide_tag_blueprint.route('/get_level_query', methods=['POST', 'GET'])
def get_level_query():
    print("In function get_level_query")
    cache_final_tag = gl.get_value("final_tag")
    contain_head_map = {}
    resp_data = []
    # 首先筛选所有总部
    for item in cache_final_tag:
        if item.headquarter_tag not in contain_head_map.keys():
            contain_head_map[str(item.headquarter_tag)] = {}
    # 再筛选所有区域
    for item in cache_final_tag:
        if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
    # 再筛选所有项目
    for item in cache_final_tag:
        if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
    for item in cache_final_tag:
        contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)
    # 将返回数据格式化
    for head in contain_head_map:
        if head != "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project if project != "None" else "其他", "value": project,
                                         "children": check_code_list})
                region_list.append(
                    {"label": region if region != "None" else "其他", "value": region, "children": project_list})
            resp_data.append({"label": head, "value": head, "children": region_list})
    for head in contain_head_map:
        if head == "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project if project != "None" else "其他", "value": project,
                                         "children": check_code_list})
                region_list.append(
                    {"label": region if region != "None" else "其他", "value": region, "children": project_list})
            resp_data.append({"label": "其他", "value": head, "children": region_list})
    print(resp_data)
    return jsonify(resp_data)


# 数据分析系统脱敏
@hide_tag_blueprint.route('/get_level_hide', methods=['POST', 'GET'])
def get_level_hide():
    print("In function get_level_hide")
    cache_final_tag = gl.get_value("final_tag")
    contain_head_map = {}
    resp_data = []
    head_hide_tag_map = {}
    region_hide_tag_map = {}
    project_hide_tag_map = {}
    # 首先筛选所有总部
    for item in cache_final_tag:
        if item.headquarter_tag not in contain_head_map.keys():
            contain_head_map[str(item.headquarter_tag)] = {}
            head_hide_tag_map[str(item.headquarter_tag)] = \
                str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(item.headquarter_tag)
    # 再筛选所有区域
    for item in cache_final_tag:
        if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
        if str(item.headquarter_tag) + '/' + str(item.region_tag) not in region_hide_tag_map.keys():
            region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = \
                str(item.region_hide_tag) if item.region_hide_tag is not None else str(item.region_tag)

    # 再筛选所有项目
    for item in cache_final_tag:
        if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
        if str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(
                item.project_tag) not in project_hide_tag_map.keys():
            project_hide_tag_map[str(item.headquarter_tag)+'/'+str(item.region_tag)+'/'+str(item.project_tag)] = \
                    str(item.project_hide_tag) if item.project_hide_tag is not None else str(item.project_tag)

    for item in cache_final_tag:
        contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)
    # 将返回数据格式化
    for head in contain_head_map:
        if head != "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project_hide_tag_map[head+'/'+region+'/'+project]
                                        if project_hide_tag_map[head+'/'+region+'/'+project] != "None" else "其他",
                                         "value": project,
                                         "children": check_code_list})
                region_list.append({"label": region_hide_tag_map[head+'/'+region]
                                    if region_hide_tag_map[head+'/'+region] != "None" else "其他",
                                    "value": region,
                                    "children": project_list})
            resp_data.append({"label": head_hide_tag_map[head] if head_hide_tag_map[head] != "None" else "其他",
                              "value": head, "children": region_list})
    for head in contain_head_map:
        if head == "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project_hide_tag_map[head + '/' + region + '/' + project]
                                        if project_hide_tag_map[head + '/' + region + '/' + project] != "None" else "其他",
                                         "value": project,
                                         "children": check_code_list})
                region_list.append({"label": region_hide_tag_map[head + '/' + region]
                                    if region_hide_tag_map[head + '/' + region] != "None" else "其他",
                                    "value": region,
                                    "children": project_list})
            resp_data.append({"label": "其他", "value": head, "children": region_list})
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_headquarter_tag', methods=['POST', 'GET'])
def get_headquarter_tag():
    print("In function get_headquarter_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        if item.headquarter_tag not in contain_map and item.headquarter_tag is not None:
            resp_data.append({"value": item.headquarter_tag, "label": item.headquarter_tag})
            contain_map.append(item.headquarter_tag)
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_headquarter_hide_tag', methods=['POST', 'GET'])
def get_headquarter_hide_tag():
    print("In function get_headquarter_hide_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        if str(item.headquarter_tag) not in contain_map and item.headquarter_tag is not None:
            resp_data.append({"value": str(item.headquarter_tag), "label": str(item.headquarter_hide_tag) if
                              item.headquarter_hide_tag is not None else str(item.headquarter_tag)})
            contain_map.append(str(item.headquarter_tag))
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_region_tag', methods=['POST', 'GET'])
def get_region_tag():
    print("In function get_region_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        if str(item.headquarter_tag) + "/" + str(item.region_tag) not in contain_map and item.region_tag is not None:
            resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                              "label": str(item.headquarter_tag) + "/" + str(item.region_tag)})
            contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_region_hide_tag', methods=['POST', 'GET'])
def get_region_hide_tag():
    print("In function get_region_hide_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        if str(item.headquarter_tag) + "/" + str(item.region_tag) not in contain_map and item.region_tag is not None:
            resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                              "label": (str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(item.headquarter_tag)) + "/" +
                                       (str(item.region_hide_tag) if item.region_hide_tag is not None else str(item.region_tag))})
            contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_project_tag', methods=['POST', 'GET'])
def get_project_tag():
    print("In function get_project_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
        if temp not in contain_map and item.project_tag is not None:
            resp_data.append({"value": temp, "label": str(item.headquarter_tag) + "/" + str(item.project_tag)})
            contain_map.append(temp)
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_project_hide_tag', methods=['POST', 'GET'])
def get_project_hide_tag():
    print("In function get_project_hide_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
        if temp not in contain_map and item.project_tag is not None:
            resp_data.append({"value": temp,
                              "label": (str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(item.headquarter_tag)) + "/" +
                                       (str(item.project_hide_tag) if item.project_hide_tag is not None else str(item.project_tag))})
            contain_map.append(temp)
    print(resp_data)
    return jsonify(resp_data)


# 9.1权限查询
@hide_tag_blueprint.route('/get_level_query_new', methods=['POST', 'GET'])
def get_level_query_new():
    print("In function get_level_query_new")
    cache_final_tag = gl.get_value("final_tag")
    user_type = request.values.get("userType")
    headquarter_tag = request.values.get("headquarter")
    region_tag = request.values.get("region")
    project_tag = request.values.get("project")
    contain_head_map = {}
    resp_data = []
    if user_type == "超级用户" or user_type == "系统用户":
        # 首先筛选所有总部
        for item in cache_final_tag:
            if item.headquarter_tag not in contain_head_map.keys():
                contain_head_map[str(item.headquarter_tag)] = {}
        # 再筛选所有区域
        for item in cache_final_tag:
            if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
        # 再筛选所有项目
        for item in cache_final_tag:
            if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
        for item in cache_final_tag:
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)
    elif user_type == "总部":
        # 首先筛选所有总部
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if item.headquarter_tag not in contain_head_map.keys():
                    contain_head_map[str(item.headquarter_tag)] = {}
        # 再筛选所有区域
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
        # 再筛选所有项目
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)

    elif user_type == "区域":
        # 首先筛选所有总部
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                if item.headquarter_tag not in contain_head_map.keys():
                    contain_head_map[str(item.headquarter_tag)] = {}
        # 再筛选所有区域
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
        # 再筛选所有项目
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)

    elif user_type == "项目":
        # 首先筛选所有总部
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                if item.headquarter_tag not in contain_head_map.keys():
                    contain_head_map[str(item.headquarter_tag)] = {}
        # 再筛选所有区域
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
        # 再筛选所有项目
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)
    # 将返回数据格式化
    for head in contain_head_map:
        if head != "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project if project != "None" else "其他", "value": project,
                                         "children": check_code_list})
                region_list.append(
                    {"label": region if region != "None" else "其他", "value": region, "children": project_list})
            resp_data.append({"label": head, "value": head, "children": region_list})
    for head in contain_head_map:
        if head == "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project if project != "None" else "其他", "value": project,
                                         "children": check_code_list})
                region_list.append(
                    {"label": region if region != "None" else "其他", "value": region, "children": project_list})
            resp_data.append({"label": "其他", "value": head, "children": region_list})
    print(resp_data)
    return jsonify(resp_data)


# 数据分析系统脱敏
@hide_tag_blueprint.route('/get_level_hide_new', methods=['POST', 'GET'])
def get_level_hide_new():
    print("In function get_level_hide_new")
    cache_final_tag = gl.get_value("final_tag")
    user_type = request.values.get("userType")
    headquarter_tag = request.values.get("headquarter")
    region_tag = request.values.get("region")
    project_tag = request.values.get("project")
    contain_head_map = {}
    resp_data = []
    head_hide_tag_map = {}
    region_hide_tag_map = {}
    project_hide_tag_map = {}
    if user_type == "超级用户" or user_type == "系统用户":
        # 首先筛选所有总部
        for item in cache_final_tag:
            if item.headquarter_tag not in contain_head_map.keys():
                contain_head_map[str(item.headquarter_tag)] = {}
                head_hide_tag_map[str(item.headquarter_tag)] = \
                    str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                        item.headquarter_tag)
        # 再筛选所有区域
        for item in cache_final_tag:
            if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
            if str(item.headquarter_tag) + '/' + str(item.region_tag) not in region_hide_tag_map.keys():
                region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = \
                    str(item.region_hide_tag) if item.region_hide_tag is not None else str(item.region_tag)

        # 再筛选所有项目
        for item in cache_final_tag:
            if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
            if str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(
                    item.project_tag) not in project_hide_tag_map.keys():
                project_hide_tag_map[
                    str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(item.project_tag)] = \
                    str(item.project_hide_tag) if item.project_hide_tag is not None else str(item.project_tag)
        # 再筛选所有检查
        for item in cache_final_tag:
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)

    elif user_type == "总部":
        # 首先筛选所有总部
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if item.headquarter_tag not in contain_head_map.keys():
                    contain_head_map[str(item.headquarter_tag)] = {}
                    head_hide_tag_map[str(item.headquarter_tag)] = \
                        str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                            item.headquarter_tag)
        # 再筛选所有区域
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
                if str(item.headquarter_tag) + '/' + str(item.region_tag) not in region_hide_tag_map.keys():
                    region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = \
                        str(item.region_hide_tag) if item.region_hide_tag is not None else str(item.region_tag)

        # 再筛选所有项目
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
                if str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(
                        item.project_tag) not in project_hide_tag_map.keys():
                    project_hide_tag_map[
                        str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(item.project_tag)] = \
                        str(item.project_hide_tag) if item.project_hide_tag is not None else str(item.project_tag)
        # 再筛选所有检查
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)

    elif user_type == "区域":
        # 首先筛选所有总部
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                if item.headquarter_tag not in contain_head_map.keys():
                    contain_head_map[str(item.headquarter_tag)] = {}
                    head_hide_tag_map[str(item.headquarter_tag)] = \
                        str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                            item.headquarter_tag)
        # 再筛选所有区域
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
                if str(item.headquarter_tag) + '/' + str(item.region_tag) not in region_hide_tag_map.keys():
                    region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = \
                        str(item.region_hide_tag) if item.region_hide_tag is not None else str(item.region_tag)

        # 再筛选所有项目
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
                if str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(
                        item.project_tag) not in project_hide_tag_map.keys():
                    project_hide_tag_map[
                        str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(item.project_tag)] = \
                        str(item.project_hide_tag) if item.project_hide_tag is not None else str(item.project_tag)
        # 再筛选所有检查
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)

    elif user_type == "项目":
        # 首先筛选所有总部
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                if item.headquarter_tag not in contain_head_map.keys():
                    contain_head_map[str(item.headquarter_tag)] = {}
                    head_hide_tag_map[str(item.headquarter_tag)] = \
                        str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                            item.headquarter_tag)
        # 再筛选所有区域
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
                if str(item.headquarter_tag) + '/' + str(item.region_tag) not in region_hide_tag_map.keys():
                    region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = \
                        str(item.region_hide_tag) if item.region_hide_tag is not None else str(item.region_tag)

        # 再筛选所有项目
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                    contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
                if str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(
                        item.project_tag) not in project_hide_tag_map.keys():
                    project_hide_tag_map[
                        str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(item.project_tag)] = \
                        str(item.project_hide_tag) if item.project_hide_tag is not None else str(item.project_tag)
        # 再筛选所有检查
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)

    # 将返回数据格式化
    for head in contain_head_map:
        if head != "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project_hide_tag_map[head+'/'+region+'/'+project]
                                        if project_hide_tag_map[head+'/'+region+'/'+project] != "None" else "其他",
                                         "value": project,
                                         "children": check_code_list})
                region_list.append({"label": region_hide_tag_map[head+'/'+region]
                                    if region_hide_tag_map[head+'/'+region] != "None" else "其他",
                                    "value": region,
                                    "children": project_list})
            resp_data.append({"label": head_hide_tag_map[head] if head_hide_tag_map[head] != "None" else "其他",
                              "value": head, "children": region_list})
    for head in contain_head_map:
        if head == "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project_hide_tag_map[head + '/' + region + '/' + project]
                                        if project_hide_tag_map[head + '/' + region + '/' + project] != "None" else "其他",
                                         "value": project,
                                         "children": check_code_list})
                region_list.append({"label": region_hide_tag_map[head + '/' + region]
                                    if region_hide_tag_map[head + '/' + region] != "None" else "其他",
                                    "value": region,
                                    "children": project_list})
            resp_data.append({"label": "其他", "value": head, "children": region_list})
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_headquarter_tag_new', methods=['POST', 'GET'])
def get_headquarter_tag_new():
    print("In function get_headquarter_tag_new")
    cache_final_tag = gl.get_value("final_tag")
    user_type = request.values.get("userType")
    headquarter_tag = request.values.get("headquarter")
    # region_tag = request.values.get("region")
    # project_tag = request.values.get("project")
    contain_map = []
    resp_data = []
    if user_type == "超级用户" or user_type == "系统用户":
        for item in cache_final_tag:
            if item.headquarter_tag not in contain_map and item.headquarter_tag is not None:
                resp_data.append({"value": item.headquarter_tag, "label": item.headquarter_tag})
                contain_map.append(item.headquarter_tag)
    elif user_type == "总部":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if item.headquarter_tag not in contain_map and item.headquarter_tag is not None:
                    resp_data.append({"value": item.headquarter_tag, "label": item.headquarter_tag})
                    contain_map.append(item.headquarter_tag)
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_headquarter_hide_tag_new', methods=['POST', 'GET'])
def get_headquarter_hide_tag_new():
    print("In function get_headquarter_hide_tag_new")
    cache_final_tag = gl.get_value("final_tag")
    user_type = request.values.get("userType")
    headquarter_tag = request.values.get("headquarter")
    # region_tag = request.values.get("region")
    # project_tag = request.values.get("project")
    contain_map = []
    resp_data = []
    if user_type == "超级用户" or user_type == "系统用户":
        for item in cache_final_tag:
            if str(item.headquarter_tag) not in contain_map and item.headquarter_tag is not None:
                resp_data.append({"value": str(item.headquarter_tag), "label": str(item.headquarter_hide_tag) if
                                  item.headquarter_hide_tag is not None else str(item.headquarter_tag)})
                contain_map.append(str(item.headquarter_tag))
    elif user_type == "总部":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if str(item.headquarter_tag) not in contain_map and item.headquarter_tag is not None:
                    resp_data.append({"value": str(item.headquarter_tag), "label": str(item.headquarter_hide_tag) if
                                      item.headquarter_hide_tag is not None else str(item.headquarter_tag)})
                    contain_map.append(str(item.headquarter_tag))
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_region_tag_new', methods=['POST', 'GET'])
def get_region_tag_new():
    print("In function get_region_tag_new")
    cache_final_tag = gl.get_value("final_tag")
    user_type = request.values.get("userType")
    headquarter_tag = request.values.get("headquarter")
    region_tag = request.values.get("region")
    # project_tag = request.values.get("project")
    contain_map = []
    resp_data = []
    if user_type == "超级用户" or user_type == "系统用户":
        for item in cache_final_tag:
            if str(item.headquarter_tag) + "/" + str(
                    item.region_tag) not in contain_map and item.region_tag is not None:
                resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                                  "label": str(item.headquarter_tag) + "/" + str(item.region_tag)})
                contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    elif user_type == "总部":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if str(item.headquarter_tag) + "/" + str(
                        item.region_tag) not in contain_map and item.region_tag is not None:
                    resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                                      "label": str(item.headquarter_tag) + "/" + str(item.region_tag)})
                    contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    elif user_type == "区域":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                if str(item.headquarter_tag) + "/" + str(
                        item.region_tag) not in contain_map and item.region_tag is not None:
                    resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                                      "label": str(item.headquarter_tag) + "/" + str(item.region_tag)})
                    contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_region_hide_tag_new', methods=['POST', 'GET'])
def get_region_hide_tag_new():
    print("In function get_region_hide_tag_new")
    cache_final_tag = gl.get_value("final_tag")
    user_type = request.values.get("userType")
    headquarter_tag = request.values.get("headquarter")
    region_tag = request.values.get("region")
    # project_tag = request.values.get("project")
    contain_map = []
    resp_data = []
    if user_type == "超级用户" or user_type == "系统用户":
        for item in cache_final_tag:
            if str(item.headquarter_tag) + "/" + str(
                    item.region_tag) not in contain_map and item.region_tag is not None:
                resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                                  "label": (
                                               str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                                                   item.headquarter_tag)) + "/" +
                                           (str(item.region_hide_tag) if item.region_hide_tag is not None else str(
                                               item.region_tag))})
                contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    elif user_type == "总部":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                if str(item.headquarter_tag) + "/" + str(
                        item.region_tag) not in contain_map and item.region_tag is not None:
                    resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                                      "label": (
                                                   str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                                                       item.headquarter_tag)) + "/" +
                                               (str(item.region_hide_tag) if item.region_hide_tag is not None else str(
                                                   item.region_tag))})
                    contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    elif user_type == "区域":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                if str(item.headquarter_tag) + "/" + str(
                        item.region_tag) not in contain_map and item.region_tag is not None:
                    resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                                      "label": (
                                                   str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                                                       item.headquarter_tag)) + "/" +
                                               (str(item.region_hide_tag) if item.region_hide_tag is not None else str(
                                                   item.region_tag))})
                    contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_project_tag_new', methods=['POST', 'GET'])
def get_project_tag_new():
    print("In function get_project_tag_new")
    cache_final_tag = gl.get_value("final_tag")
    user_type = request.values.get("userType")
    headquarter_tag = request.values.get("headquarter")
    region_tag = request.values.get("region")
    project_tag = request.values.get("project")
    contain_map = []
    resp_data = []
    if user_type == "超级用户" or user_type == "系统用户":
        for item in cache_final_tag:
            temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
            if temp not in contain_map and item.project_tag is not None:
                resp_data.append({"value": temp, "label": str(item.headquarter_tag) + "/" + str(item.project_tag)})
                contain_map.append(temp)
    elif user_type == "总部":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
                if temp not in contain_map and item.project_tag is not None:
                    resp_data.append({"value": temp, "label": str(item.headquarter_tag) + "/" + str(item.project_tag)})
                    contain_map.append(temp)
    elif user_type == "区域":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
                if temp not in contain_map and item.project_tag is not None:
                    resp_data.append({"value": temp, "label": str(item.headquarter_tag) + "/" + str(item.project_tag)})
                    contain_map.append(temp)
    elif user_type == "项目":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
                if temp not in contain_map and item.project_tag is not None:
                    resp_data.append({"value": temp, "label": str(item.headquarter_tag) + "/" + str(item.project_tag)})
                    contain_map.append(temp)
    print(resp_data)
    return jsonify(resp_data)


@hide_tag_blueprint.route('/get_project_hide_tag_new', methods=['POST', 'GET'])
def get_project_hide_tag_new():
    print("In function get_project_hide_tag_new")
    cache_final_tag = gl.get_value("final_tag")
    user_type = request.values.get("userType")
    headquarter_tag = request.values.get("headquarter")
    region_tag = request.values.get("region")
    project_tag = request.values.get("project")
    contain_map = []
    resp_data = []
    if user_type == "超级用户" or user_type == "系统用户":
        for item in cache_final_tag:
            temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
            if temp not in contain_map and item.project_tag is not None:
                resp_data.append({"value": temp,
                                  "label": (
                                               str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                                                   item.headquarter_tag)) + "/" +
                                           (str(item.project_hide_tag) if item.project_hide_tag is not None else str(
                                               item.project_tag))})
                contain_map.append(temp)
    elif user_type == "总部":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag:
                temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
                if temp not in contain_map and item.project_tag is not None:
                    resp_data.append({"value": temp,
                                      "label": (
                                                   str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                                                       item.headquarter_tag)) + "/" +
                                               (
                                                   str(item.project_hide_tag) if item.project_hide_tag is not None else str(
                                                       item.project_tag))})
                    contain_map.append(temp)
    elif user_type == "区域":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag:
                temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
                if temp not in contain_map and item.project_tag is not None:
                    resp_data.append({"value": temp,
                                      "label": (
                                                   str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                                                       item.headquarter_tag)) + "/" +
                                               (
                                                   str(item.project_hide_tag) if item.project_hide_tag is not None else str(
                                                       item.project_tag))})
                    contain_map.append(temp)
    elif user_type == "项目":
        for item in cache_final_tag:
            if item.headquarter_tag == headquarter_tag and item.region_tag == region_tag and item.project_tag == project_tag:
                temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
                if temp not in contain_map and item.project_tag is not None:
                    resp_data.append({"value": temp,
                                      "label": (
                                                   str(item.headquarter_hide_tag) if item.headquarter_hide_tag is not None else str(
                                                       item.headquarter_tag)) + "/" +
                                               (
                                                   str(item.project_hide_tag) if item.project_hide_tag is not None else str(
                                                       item.project_tag))})
                    contain_map.append(temp)
    print(resp_data)
    return jsonify(resp_data)
