import logging
log = logging.getLogger()

import time
from datetime import datetime

def AM2302(db):
    def handler(data):
        try:
            db['AM2302'].insert_one({"_id": (int(time.time() / 300) * 300),
                                     'temperature': round(float(data[1]), 1),
                                     'humidity': round(float(data[0]), 1),
                                     'time': datetime.now(),
                                     })
        except Exception as err:
            log.error(err)
    return handler

def electricity(db):
    def handler(data):
        if data.status_code == 200:
            json = data.json()
            try:
                dt = datetime.strptime(json['data']['last_update'], "%Y-%m-%d %H:%M:%S")
                remain = float(json['data']['remain'])
                log.debug("{0} {1}".format(dt, remain))
                db['electricity'].insert_one({"_id": str(dt.date()),
                                              'remain': remain,
                                              'time': dt})
            except Exception as err:
                log.error(err)
    return handler
                                           

def initDataRecorder(db, dataSources):
    # dataSources['CPUTemp'].attach('recorder', temperature(db))
    dataSources['AM2302'].attach('recorder', AM2302(db))
    dataSources['Elec'].attach('recorder', electricity(db))

