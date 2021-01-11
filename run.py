from ops import app_create
from datetime import datetime
from models.new_cascade_risk_prj_danger_record import NewCascadeRiskPrjDangerRecord
from models.risk_user import RiskUser
from models.project_with_tag import PrjWithTag
import functions.cache_data as gl
from flask_cors import CORS

app = app_create('testing')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app, supports_credentials=True)
@app.before_first_request
def cache_tables():
    print("In func cache_tables")
    start_t = datetime.now()
    gl._init()

    # 缓存表 risk_user
    cache_risk_user = RiskUser.query.all()
    end_t1 = datetime.now()
    gl.set_value("cache_risk_user", cache_risk_user)
    print("Time to query table 1 is " + str((end_t1 - start_t).seconds) + "s")
    print(cache_risk_user[0])

    # 缓存表 prj_with_tag
    cache_prj_with_tag = PrjWithTag.query.all()
    end_t2 = datetime.now()
    gl.set_value("cache_prj_with_tag", cache_prj_with_tag)
    print("Time to query table 2 is " + str((end_t2 - end_t1).seconds) + "s")
    print(cache_prj_with_tag[0])

    # 缓存表 new_cascade_risk_prj_danger_record
    cache_cascade_record = NewCascadeRiskPrjDangerRecord.query.all()
    end_t3 = datetime.now()
    gl.set_value("cache_cascade_record", cache_cascade_record)
    print("Time to query table 3 is " + str((end_t3 - end_t2).seconds) + "s")

    cache_check_location_map = {}
    for item in cache_cascade_record:
        if item.project_code not in cache_check_location_map.keys():
            cache_check_location_map[item.project_code] = {"lat": item.lat, "lng": item.lng}
    gl.set_value("cache_check_location_map", cache_check_location_map)

    end_t = datetime.now()
    print("Time to query all is " + str((end_t - start_t).seconds) + "s")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
