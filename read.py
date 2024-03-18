import pickle
import json
from pprint import pprint
import PPv16
from _for import TS, TSLocation
from _ct import DisruptionReasonType
from pyxb.binding import datatypes

# event types
# schedule - sch3:Schedule
# deactivated - sch2:DeactivatedSchedule
# association - sch2:Association
# scheduleFormations - fm2:ScheduleFormations
# TS - for:TS
# formationLoading - fm:Loading
# OW - sm:StationMessage
# trainAlert - ta:TrainAlert
# trainOrder - tor:TrainOrder
# trackingID - td:TrackingID
# alarm - alm:RTTIAlarm

events = [
    "schedule",
    "deactivated",
    "association",
    "scheduleFormations",
    "TS",
    "formationLoading",
    "OW",
    "trainAlert",
    "trainOrder",
    "trackingID",
    "alarm",
]

FILE = "msg.pkl"

with open(FILE, "rb") as f:
    msg = pickle.load(f)


def hasMessage(obj: PPv16.DataResponse, message: str) -> bool:
    return hasattr(obj, message) and len(getattr(obj, message)) > 0


for m in msg:
    print()
    # type of object
    print(type(m))
    # print the object
    print(m)
    # print the timestamp
    print(m.ts)
    # print every property
    # for prop in dir(m):
    #     if not prop.startswith("_"):
    #         print(prop, getattr(m, prop))

    if not m.uR:
        # no message in response
        continue

    print("===== uR =====")
    uR: PPv16.DataResponse = m.uR
    # get events that are not empty arrays
    # for e in events:
    #     theseEvents = getattr(uR, e)
    #     print(f"=== {e} ===")
    #     print(theseEvents)
    #     for thisEvent in theseEvents:
    #         print(thisEvent)
    #         for prop in dir(thisEvent):
    #             if not prop.startswith("_"):
    #                 print(prop, getattr(thisEvent, prop))

    if hasMessage(uR, "TS"):
        print("=== TS ===")
        for ts in uR.TS:
            ts: TS
            # data type from _for.py
            isReverseFormation: datatypes.boolean = ts.isReverseFormation
            # data type from _ct.py
            #  how to set this as an array of DisruptionReasonType?
            LateReasons = ts.LateReason
            Locations = ts.Location
            rid = ts.rid
            ssd = ts.ssd
            uid = ts.uid

            for Loc in Locations:
                Loc: TSLocation
                tpl = Loc.tpl
                pass_ = Loc.pass_
                arr = Loc.arr
                dep = Loc.dep
                plat = Loc.plat
                suppr = Loc.suppr
                length = Loc.length
                detachFront = Loc.detachFront
                wta = Loc.wta
                wtd = Loc.wtd
                wtp = Loc.wtp
                pta = Loc.pta
                ptd = Loc.ptd
