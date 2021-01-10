from ops import app_create
from datetime import datetime
from models.new_cascade_risk_prj_danger_record import NewCascadeRiskPrjDangerRecord
from models.risk_user import RiskUser
from models.project_with_tag import PrjWithTag
import functions.cache_data as gl

app = app_create('testing')


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
    # cache_new_cascade_record = NewCascadeRiskPrjDangerRecord.query.all()
    # end_t3 = datetime.now()
    # print("Time to query table 3 is " + str((end_t3 - end_t2).seconds) + "s")
    # print(cache_new_cascade_record[0])

    end_t = datetime.now()
    print("Time to query all is " + str((end_t - start_t).seconds) + "s")


if __name__ == '__main__':
    app.run(debug=True)
