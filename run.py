from ops import app_create
from datetime import datetime
from models.new_cascade_risk_prj_danger_record import NewCascadeRiskPrjDangerRecord
from models.final_all_record import FinalAllRecord
from models.risk_user import RiskUser
from models.project_with_tag import PrjWithTag
from models.sys_file import SysFile
# dict 字典 map key-value
import functions.cache_data as gl
from flask_cors import CORS
import random

# modified
from models.final_record import FinalRecord
from models.final_tag import FinalTag
from models.risk_project import RiskProject

app = app_create('testing')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app, supports_credentials=True)
@app.before_first_request
def cache_tables():
    print("In func cache_tables")
    start_t = datetime.now()
    gl._init()

    # 缓存表 risk_user
    begin_t = datetime.now()
    cache_risk_user = RiskUser.query.all()
    gl.set_value("risk_user", cache_risk_user)
    print("Time to query table [1]risk_user is " + str((datetime.now() - begin_t).seconds) + "s")
    print(cache_risk_user[0])

    # 缓存表 prj_with_tag
    # cache_prj_with_tag = PrjWithTag.query.all()
    # end_t2 = datetime.now()
    # gl.set_value("cache_prj_with_tag", cache_prj_with_tag)
    # print("Time to query table 2 is " + str((end_t2 - end_t1).seconds) + "s")
    # print(cache_prj_with_tag[0])

    # 缓存表 new_cascade_risk_prj_danger_record
    # cache_cascade_record = NewCascadeRiskPrjDangerRecord.query.all()
    # cache_cascade_record = FinalAllRecord.query.all()
    # end_t3 = datetime.now()
    # gl.set_value("cache_cascade_record", cache_cascade_record)
    # print("Time to query table 3 is " + str((end_t3 - end_t2).seconds) + "s")

    # 缓存表 sys_file
    begin_t = datetime.now()
    cache_sys_file = SysFile.query.all()
    gl.set_value("sys_file", cache_sys_file)
    print("Time to query [2]sys_file is " + str((datetime.now() - begin_t).seconds) + "s")

    # cache_check_location_map = {}
    # for item in cache_cascade_record:
    #     if item.project_code not in cache_check_location_map.keys():
    #         cache_check_location_map[item.project_code] = {"lat": item.lat, "lng": item.lng, "index": round(random.uniform(1.0, 99.99), 2)}
    # gl.set_value("cache_check_location_map", cache_check_location_map)

    # modified
    begin_t = datetime.now()
    cache_final_record = FinalRecord.query.all()
    gl.set_value("final_record", cache_final_record)
    print("Time to query [3]final_record is " + str((datetime.now() - begin_t).seconds) + "s")

    begin_t = datetime.now()
    cache_final_tag = FinalTag.query.all()
    gl.set_value("final_tag", cache_final_tag)
    print("Time to query [4]final_tag is " + str((datetime.now() - begin_t).seconds) + "s")

    begin_t = datetime.now()
    cache_risk_project = RiskProject.query.all()
    gl.set_value("risk_project", cache_risk_project)
    print("Time to query [5]risk_project is " + str((datetime.now() - begin_t).seconds) + "s")

    end_t = datetime.now()
    print("Time to query all is " + str((end_t - start_t).seconds) + "s")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
