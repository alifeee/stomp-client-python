"""read from pickle file and print way too much data"""

import pickle
from typing import List
from pyxb.binding import datatypes
from PPv16 import CTD_ANON_2, DataResponse
from _for import TS, TSLocation, TSTimeData, PlatformData, STD_ANON
from _ct import (
    TiplocType,
    TrainLengthType,
    RIDType,
    RTTIDateType,
    UIDType,
    DisruptionReasonType,
    WTimeType,
    RTTITimeType,
    SourceTypeInst,
    PlatformType,
)
from _sch3 import Schedule, OR

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


def hasMessage(obj: DataResponse, message: str) -> bool:
    return hasattr(obj, message) and len(getattr(obj, message)) > 0


for m in msg:
    m: CTD_ANON_2
    print()
    print()
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
    uR: DataResponse = m.uR
    # get events that are not empty arrays
    for e in events:
        theseEvents = getattr(uR, e)
        #     print(f"=== {e} ===")
        # print(theseEvents)
        for thisEvent in theseEvents:
            print(thisEvent)
    #         for prop in dir(thisEvent):
    #             if not prop.startswith("_"):
    #                 print(prop, getattr(thisEvent, prop))

    if hasMessage(uR, "TS"):
        for ts in uR.TS:
            # data type from _for.py
            ts: TS
            print(ts.toxml())
            print("=== TS ===")

            # "RTTI unique Train Identifier"
            rid: RIDType = ts.rid
            # "Train UID"
            uid: UIDType = ts.uid
            # "Scheduled Start Date"
            ssd: RTTIDateType = ts.ssd

            # "Update of forecast data for an individual location in the service's schedule"
            Locations: List[TSLocation] = ts.Location
            # "Late running reason for this service. The reason applies to all locations of this service."
            LateReasons: DisruptionReasonType = ts.LateReason
            # "Indicates whether a train that divides is working with portions in reverse to their normal formation. The value applies to the whole train. Darwin will not validate that a divide association actually exists for this service."
            isReverseFormation: datatypes.boolean = ts.isReverseFormation

            print(f"rid: {rid} \tuid: {uid} \tssd: {ssd}")
            print(
                f"LateReasons: {LateReasons} \tisReverseFormation: {isReverseFormation}"
            )

            for Loc in Locations:
                # "Tiploc Type (This is the short version of a TIPLOC - without spaces)"
                tpl: TiplocType = Loc.tpl
                # "Forecast data for the arrival at this location"
                arr: TSTimeData = Loc.arr
                # "Forecast data for the departure at this location"
                dep: TSTimeData = Loc.dep
                # "Forecast data for the pass of this location"
                pass_: TSTimeData = Loc.pass_
                # "Current platform number"
                plat: PlatformData = Loc.plat
                # "The service is suppressed at this location."
                suppr: datatypes.boolean = Loc.suppr
                # "The length of the service at this location on departure (or arrival at destination). The default value of zero indicates that the length is unknown."
                length: TrainLengthType = Loc.length
                # "Indicates from which end of the train stock will be detached. The value is set to “true” if stock will be detached from the front of the train at this location. It will be set at each location where stock will be detached from the front. Darwin will not validate that a stock detachment activity code applies at this location."
                detachFront: datatypes.boolean = Loc.detachFront

                # "Working time of arrival."
                wta: WTimeType = Loc.wta
                # "Working time of departure."
                wtd: WTimeType = Loc.wtd
                # "Working time of pass."
                wtp: WTimeType = Loc.wtp
                # "Public time of arrival."
                pta: RTTITimeType = Loc.pta
                # "Public time of departure."
                ptd: RTTITimeType = Loc.ptd

                print(f"== tpl: {tpl} ==")
                if suppr or length or detachFront:
                    print(
                        f"\tsuppr: {suppr} \tlength: {length} \tdetachFront: {detachFront}"
                    )
                if wta or wtd or wtp:
                    print(f"\twta: {wta} \twtd: {wtd} \twtp: {wtp}")
                if pta or ptd:
                    print(f"\tpta: {pta} \tptd: {ptd}")
                if arr:
                    # "Estimated Time. For locations that are public stops, this will be based on the "public schedule". For operational stops and passing locations, it will be based on the "working schedule". It is only published where there is a corresponding "activity" for the service."
                    et: RTTITimeType = arr.et
                    # "The estimated time based on the "working schedule". This will only be set for public stops when (i) it also differs from the estimated time based on the "public schedule", or (ii) where there is an operational "activity" but no public "activity"."
                    wet: RTTITimeType = arr.wet
                    # "Actual Time"
                    at: RTTITimeType = arr.at
                    # "If true, indicates that an actual time ("at") value has just been removed and replaced by an estimated time ("et"). Note that this attribute will only be set to "true" once, when the actual time is removed, and will not be set in any snapshot."
                    atRemoved: datatypes.boolean = arr.atRemoved
                    # "The class of the actual time."
                    atClass: datatypes.string = arr.atClass
                    # "The manually applied lower limit that has been applied to the estimated time at this location. The estimated time will not be set lower than this value, but may be set higher."
                    etmin: RTTITimeType = arr.etmin
                    # "Indicates that an unknown delay forecast has been set for the estimated time at this location. Note that this value indicates where a manual unknown delay forecast has been set, whereas it is the "delayed" attribute that indicates that the actual forecast is "unknown delay"."
                    etUnknown: datatypes.boolean = arr.etUnknown
                    # "Indicates that this estimated time is a forecast of "unknown delay". Displayed  as "Delayed" in LDB. Note that this value indicates that this forecast is "unknown delay", whereas it is the "etUnknown" attribute that indicates where the manual unknown delay forecast has been set."
                    delayed: datatypes.boolean = arr.delayed
                    # "The source of the forecast or actual time."
                    src: datatypes.string = arr.src
                    # "The RTTI CIS code of the CIS instance if the src is a CIS."
                    srcInst: SourceTypeInst = arr.srcInst

                    print(f"\tarr from {arr.src}:")
                    print(
                        f"\t\tet: {et} \twet: {wet} \tetmin: {etmin} \tetUnkown: {etUnknown}"
                    )
                    if at or atRemoved or atClass:
                        print(
                            f"\t\tat: {at} \tatRemoved: {atRemoved} \tatClass: {atClass}"
                        )
                    if delayed:
                        print(f"\t\tdelayed: {delayed}")
                if dep:
                    print(f"\tdep from {dep.src}:")
                    print(
                        f"\t\tet: {dep.et} \twet: {dep.wet} \tetmin: {dep.etmin} \tetUnkown: {dep.etUnknown}"
                    )
                    if dep.at or dep.atRemoved or dep.atClass:
                        print(
                            f"\t\tat: {dep.at} \tatRemoved: {dep.atRemoved} \tatClass: {dep.atClass}"
                        )
                    if dep.delayed:
                        print(f"\t\tdelayed: {dep.delayed}")
                if pass_:
                    print(f"\tpass from {pass_.src}:")
                    print(
                        f"\t\tet: {pass_.et} \twet: {pass_.wet} \tetmin: {pass_.etmin} \tetUnkown: {pass_.etUnknown}"
                    )
                    if pass_.at or pass_.atRemoved or pass_.atClass:
                        print(
                            f"\t\tat: {pass_.at} \tatRemoved: {pass_.atRemoved} \tatClass: {pass_.atClass}"
                        )
                    if pass_.delayed:
                        print(f"\t\tdelayed: {pass_.delayed}")
                if plat:
                    # "Platform number with associated flags"
                    # PlatformType: "Defines a platform number"
                    platform: PlatformType = plat.value()
                    # "Platform number is suppressed and should not be displayed."
                    platsup: datatypes.boolean = plat.platsup
                    # "Whether a CIS, or Darwin Workstation, has set platform suppression at this location."
                    cisPlatsup: datatypes.boolean = plat.cisPlatsup
                    # "The source of the platfom number. P = Planned, A = Automatic, M = Manual."
                    platsrc: STD_ANON = plat.platsrc
                    # "True if the platform number is confirmed."
                    conf: datatypes.boolean = plat.conf

                    print(f"\tplatform: {platform} \tplatsrc: {platsrc} \tconf: {conf}")
                    if platsup or cisPlatsup:
                        print(f"\t\tplatsuppress: {platsup} \tcisPlatsup: {cisPlatsup}")

    if hasMessage(uR, "schedule"):
        for schedule in uR.schedule:
            # data type from _sch3.py
            schedule: Schedule
            print(schedule.toxml())
            print("=== Schedule ===")

            cancelReason = schedule.cancelReason
            rid = schedule.rid
            uid = schedule.uid
            trainId = schedule.trainId
            rsid = schedule.rsid
            ssd = schedule.ssd
            toc = schedule.toc
            status = schedule.status
            trainCat = schedule.trainCat
            isPassengerSvc = schedule.isPassengerSvc
            isActive = schedule.isActive
            deleted = schedule.deleted
            isCharter = schedule.isCharter

            # SchedLocAttributes are
            # tpl, act, planAct, can, fid
            # CallPtAttributes are
            # pta, ptd, avgLoading

            # "Defines a Passenger Origin Calling Point"
            # @ SchedLocAttributes, CallPtAttributes
            # wta, wtd, fd
            ORS: List[OR] = schedule.OR
            if hasMessage(schedule, "OR"):
                print("== ORIGIN CALLING POINTS ==")
                for OR_ in ORS:
                    print(f" tpl: {OR_.tpl} \tact: {OR_.act} \tplanAct: {OR_.planAct}")
                    if OR_.can:
                        print(f"\tcan: {OR_.can}")
                    if OR_.fid:
                        print(f"\tfid: {OR_.fid}")
                    print(f"\tpta: {OR_.pta} \tptd: {OR_.ptd}")
                    if OR_.avgLoading:
                        print(f"\tavgLoading: {OR_.avgLoading}")
                    print(f"\twta: {OR_.wta} \twtd: {OR_.wtd}")
                    if OR_.fd:
                        print(f"\tfd: {OR_.fd}")

            # "Defines an Operational Origin Calling Point"
            # @ SchedLocAttributes
            # wta, wtd
            OPORS = schedule.OPOR
            if hasMessage(schedule, "OPOR"):
                print("== OPERATIONAL ORIGIN CALLING POINTS ==")
                for OPOR in OPORS:
                    print(
                        f" tpl: {OPOR.tpl} \tact: {OPOR.act} \tplanAct: {OPOR.planAct}"
                    )
                    if OPOR.can:
                        print(f"\tcan: {OPOR.can}")
                    if OPOR.fid:
                        print(f"\tfid: {OPOR.fid}")
                    print(f"\twta: {OPOR.wta} \twtd: {OPOR.wtd}")

            # "Defines aPassenger Intermediate Calling Point"
            # @ SchedLocAttributes, CallPtAttributes
            # wta, wtd, rdelay, fd
            IPS = schedule.IP
            if hasMessage(schedule, "IP"):
                print("== INTERMEDIATE CALLING POINTS ==")
                for IP in IPS:
                    print(f" tpl: {IP.tpl} \tact: {IP.act} \tplanAct: {IP.planAct}")
                    if IP.can:
                        print(f"\tcan: {IP.can}")
                    if IP.fid:
                        print(f"\tfid: {IP.fid}")
                    print(f"\tpta: {IP.pta} \tptd: {IP.ptd}")
                    if IP.avgLoading:
                        print(f"\tavgLoading: {IP.avgLoading}")
                    print(f"\twta: {IP.wta} \twtd: {IP.wtd}")
                    if IP.fd:
                        print(f"\tfd: {IP.fd}")
                    if IP.rdelay:
                        print(f"\trdelay: {IP.rdelay}")

            # "Defines an Operational Intermediate Calling Point"
            # @ SchedLocAttributes
            # wta, wtd, rdelay
            OPIPS = schedule.OPIP
            if hasMessage(schedule, "OPIP"):
                print("== OPERATIONAL INTERMEDIATE CALLING POINTS ==")
                for OPIP in OPIPS:
                    print(
                        f" tpl: {OPIP.tpl} \tact: {OPIP.act} \tplanAct: {OPIP.planAct}"
                    )
                    if OPIP.can:
                        print(f"\tcan: {OPIP.can}")
                    if OPIP.fid:
                        print(f"\tfid: {OPIP.fid}")
                    print(f"\twta: {OPIP.wta} \twtd: {OPIP.wtd}")
                    if OPIP.rdelay:
                        print(f"\trdelay: {OPIP.rdelay}")

            # "Defines an Intermediate Passing Point"
            # @ SchedLocAttributes
            # wtp, rdelay
            PPS = schedule.PP
            if hasMessage(schedule, "PP"):
                print("== PASSING POINTS ==")
                for PP in PPS:
                    print(f" tpl: {PP.tpl} \tact: {PP.act} \tplanAct: {PP.planAct}")
                    if PP.can:
                        print(f"\tcan: {PP.can}")
                    if PP.fid:
                        print(f"\tfid: {PP.fid}")
                    print(f"\twtp: {PP.wtp}")
                    if PP.rdelay:
                        print(f"\trdelay: {PP.rdelay}")

            # "Defines a Passenger Destination Calling point"
            # @ SchedLocAttributes, CallPtAttributes
            # wta, wtd, rdelay
            DTS = schedule.DT
            if hasMessage(schedule, "DT"):
                print("== DESTINATION CALLING POINTS ==")
                for DT in DTS:
                    print(f" tpl: {DT.tpl} \tact: {DT.act} \tplanAct: {DT.planAct}")
                    if DT.can:
                        print(f"\tcan: {DT.can}")
                    if DT.fid:
                        print(f"\tfid: {DT.fid}")
                    print(f"\tpta: {DT.pta} \tptd: {DT.ptd}")
                    if DT.avgLoading:
                        print(f"\tavgLoading: {DT.avgLoading}")
                    print(f"\twta: {DT.wta} \twtd: {DT.wtd}")
                    if DT.rdelay:
                        print(f"\trdelay: {DT.rdelay}")

            # "Defines an Operational Destination Calling point"
            # @ SchedLocAttributes
            # wta, wtd, rdelay
            OPDTS = schedule.OPDT
            if hasMessage(schedule, "OPDT"):
                print("== OPERATIONAL DESTINATION CALLING POINTS ==")
                for OPDT in OPDTS:
                    print(
                        f" tpl: {OPDT.tpl} \tact: {OPDT.act} \tplanAct: {OPDT.planAct}"
                    )
                    if OPDT.can:
                        print(f"\tcan: {OPDT.can}")
                    if OPDT.fid:
                        print(f"\tfid: {OPDT.fid}")
                    print(f"\twta: {OPDT.wta} \twtd: {OPDT.wtd}")
                    if OPDT.rdelay:
                        print(f"\trdelay: {OPDT.rdelay}")
