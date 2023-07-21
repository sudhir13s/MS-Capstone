import collections
import json
import random
import time
import timeit
import statistics
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go

CONTROLLER = {}
CONTROLLER_ACTION = {}
OCCUPANT = {}

class Event:
    def __init__(self, _time, fc1=None, fmd=None, bc1=None, bmd=None,
                 dc=None, dl=None, vs1=None, vs2=None, uss1=None, uss2=None):
        self.fmd = fmd
        self.fc1 = fc1
        self.dc = dc
        self.dl = dl
        self.vs1 = vs1
        self.uss1 = uss1

        self.bc1 = bc1
        self.bmd = bmd
        self.uss2 = uss2
        self.vs2 = vs2
        self.controller = None
        self._time = _time

    def __str__(self):
        d = {
            "FC1": self.fc1,
            "FMD": self.fmd,
            "BC1": self.bc1,
            "BMD": self.bmd,
            "DC": self.dc,
            "DL": self.dl,
            "VS1": self.vs1,
            "VS2": self.vs2,
            "USS1": self.uss1,
            "USS2": self.uss2,
            "TIME": self._time,
            "CONTROLLER": self.controller
        }
        return str(d)
        # return "fFC1: {self.front_camera1}, " \
        #        f"BC1: {self.back_camera1}, " \
        #        f"DC: {self.door_camera}, " \
        #        f"DL: {self.door_lock}, " \
        #        f"RFID: {self.rfid1}, " \
        #        f"SW: {self.sw1}"


def main():
    FRONT_CAMERA1 = ["PASS", "ALERT", ""]
    FMD = [[10, 2], [2, 10], []]
    DOOR_CAMERA = ["PASS", "ALERT", ""]
    DOOR_LOCK = ["PASS", "ALERT", ""]

    IVS1 = ["ALERT", ]
    USS1 = [[8, 2], [1, 9], []]

    BACK_CAMERA1 = ["PASS", "ALERT", "", "", "", "", ""]
    BMD = [5, "", "", "", ""]
    USS2 = [2, "", "", "", ""]
    IVS2 = ["ALERT", "", ""]
    TIME = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
            13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    # TIME = [1, 6, 12, 18, 22]

    CONTROLLER = {}
    CONTROLLER_ACTION = {}
    ALERT = "ALERT"
    PASS = "PASS"
    NO_ACTION = "NO ACTION"

    ctl_action1 = ["LIGHT: ON", "OWNER: ALERT"]  # FORCEFUL ENTER
    ctl_action2 = ["LIGHT: ON", "TV: ON", "TS: SET TEMP"]  # ENTER ANYTIME
    ctl_action3 = ["LIGHT: ON", "TV: ON", "TS: SET TEMP", "WH: ON"]  # MORNING ENTER

    ctl_action4 = ["LIGHT: OFF", "TV: OFF", "TS: SET TEMP", "WH: OFF"]  # LEAVING

    ctl_action5 = ["LIGHT: ON", "TV: ON"]  # AFTERNOON - INTERNAL ACTIVITY
    ctl_action6 = ["LIGHT: OFF", "TV: OFF"]  # NO INTERNAL ACTIVITY

    ctl_action7 = ["LIGHT: ON"]  # NIGHT - INTERNAL ACTIVITY
    ctl_action8 = ["LIGHT: OFF"]  # NIGHT - NO INTERNAL ACTIVITY

    EXEC_TIME = []
    START_TIME = []
    END_TIME = []

    for i in range(1):
        start = timeit.default_timer()
        for fmd in FMD:
            for fc in FRONT_CAMERA1:
                for dc in DOOR_CAMERA:
                    for dl in DOOR_LOCK:
                        for uss1 in USS1:
                            tm = random.choice(TIME)
                            event = Event(fmd=fmd, fc1=fc, dc=dc,
                                          dl=dl, uss1=uss1, _time=tm)
                            controller_work(event)
                            end = timeit.default_timer()
                            # START_TIME.append(start)
                            # END_TIME.append(end)
                            EXEC_TIME.append(end - start)





    # for i in range(500):
        # front_camera1, fmd, back_camera1, bmd, door_camera, door_lock, ivs1, ivs2, imd1, _time = \
        #     random.choice(FRONT_CAMERA1), random.choice(FMD), random.choice(BACK_CAMERA1), \
        #     random.choice(BMD), random.choice(DOOR_CAMERA), random.choice(DOOR_LOCK), \
        #     random.choice(IVS1), random.choice(IVS2), random.choice(USS1), random.choice(TIME)
        #
        # event = Event(front_camera1, fmd, back_camera1, bmd, door_camera, door_lock, ivs1,
        #               ivs2, imd1, imd1, _time)

    # for k, v in CONTROLLER.items():
    #     if CONTROLLER_ACTION[k] == NO_ACTION:
    #         print(k, v)
    #         print(CONTROLLER_ACTION[k])
    # print(CONTROLLER)
    # print(CONTROLLER_ACTION)
    # return CONTROLLER, CONTROLLER_ACTION
    print(EXEC_TIME)
    print(len(EXEC_TIME))
    # print(statistics.mean(EXEC_TIME))


def Ascending(A): # Ascending order
    for i in range(len(A) - 1):
        if A[i] - A[i+1] > 0:
            return False
    return True


def Descending(A): # Descending order
    for i in range(len(A) - 1):
        if A[i] - A[i+1] < 0:
            return False
    return True


def controller_work(event):
    global CONTROLLER
    global CONTROLLER_ACTION
    ALERT = "ALERT"
    PASS = "PASS"
    NO_ACTION = "NO_ACTION"


    ctl_action1 = ["LIGHT: ON", "OWNER: ALERT"]  # FORCEFUL ENTER
    ctl_action2 = ["LIGHT: ON", "TV: ON", "TS: SET TEMP"]  # ENTER ANYTIME
    ctl_action3 = ["LIGHT: ON", "TV: ON", "TS: SET TEMP", "WH: ON"]  # MORNING ENTER

    ctl_action4 = ["LIGHT: OFF", "TV: OFF", "TS: SET TEMP", "WH: OFF"]  # LEAVING

    ctl_action5 = ["LIGHT: ON", "TV: ON"]  # AFTERNOON - INTERNAL ACTIVITY
    ctl_action6 = ["LIGHT: OFF", "TV: OFF"]  # NO INTERNAL ACTIVITY

    ctl_action7 = ["LIGHT: ON"]  # NIGHT - INTERNAL ACTIVITY
    ctl_action8 = ["LIGHT: OFF"]  # NIGHT - NO INTERNAL ACTIVITY

    # EVENT - FORCEFUL ENTER
    if (event.fc1 == ALERT and event.dc == ALERT) or \
            (event.fc1 == ALERT and event.dl == ALERT) or \
            (event.dl == ALERT and event.dc == ALERT):
        # FRONT BREAK-IN
        # if event._time in [0, 1, 2, 3, 4, 5, 21, 22, 23]:
        #     event._time = "NIGHT"
        # else:
        #     event._time = "DAY"
        event.vs1, event.vs2, event.bc1, event.bmd = "", "", "", ""
        # event.uss1 = 2
        event.controller = "FRONT_BREAK_IN"
        CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
        CONTROLLER_ACTION[str(event)] = ctl_action1
        print(event)

    elif event.bc1 == ALERT and (event.vs1 or event.vs2) and \
            event.fc1 != ALERT and event.dc != ALERT and event.dl \
            != ALERT:
        # BACK BREAK-IN
        # if event._time in [0, 1, 2, 3, 4, 5, 21, 22, 23]:
        #     event._time = "NIGHT"
        # else:
        #     event._time = "DAY"
        event.fc1, event.fmd, event.dc, event.dl = "", "", "", ""
        # event.uss1 = [5]
        event.controller = "BACK_BREAK_IN"
        CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
        CONTROLLER_ACTION[str(event)] = ctl_action1
        print(event)
    # EVENT - OWNER ENTERING/LEAVING HOUSE
    elif (event.fmd or event.uss1) and (event.fc1 == PASS and event.dc == PASS) or \
            (event.fc1 == PASS and event.dl == PASS) or \
            (event.dc == PASS and event.dl == PASS):
        # OWNER ENTERING HOUSE
        if Descending(event.fmd):
            event.vs1, event.vs2, event.bc1, event.bmd = "", "", "", ""
            if not event.uss1: event.uss1 = []
            event.controller = "OWNER_ENTER"
            print(event)
            if event._time in range(6, 9):
                # event._time = "MORNING"
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ctl_action3
            else:
                # if event._time in [0, 1, 2, 3, 4, 5, 21, 22, 23]:
                #     event._time = "NIGHT"
                # else:
                #     event._time = "DAY"

                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ctl_action2
        # OWNER LEAVING HOUSE
        elif Ascending(event.uss1):
            event.vs1, event.vs2, event.bc1, event.bmd = "", "", "", ""
            # event.uss1, event.dl = "", ""
            if not event.fmd: event.fmd = []
            event.controller = "OWNER_LEAVE"
            print(event)
            # if event._time in [0, 1, 2, 3, 4, 5, 6, 21, 22, 23]:
            #     event._time = "NIGHT"
            # else:
            #     event._time = "DAY"
            CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
            CONTROLLER_ACTION[str(event)] = ctl_action4
        elif event.dl == PASS:
            event.vs1, event.vs2, event.bc1, event.bmd = "", "", "", ""
            # event.uss1, event.dl = "", ""
            if not event.fmd: event.fmd = []
            event.controller = "OWNER_ENTER"
            print(event)
            # if event._time in [0, 1, 2, 3, 4, 5, 6, 21, 22, 23]:
            #     event._time = "NIGHT"
            # else:
            #     event._time = "DAY"
            CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
            CONTROLLER_ACTION[str(event)] = ctl_action4
        else:
            event.vs1, event.vs2, event.bc1, event.bmd = "", "", "", ""
            event.dl = ""
            # event.uss1, event.dl = "", ""
            if not event.uss1: event.uss1 = []
            event.controller = "OWNER_LEAVE"
            print(event)
            # if event._time in [0, 1, 2, 3, 4, 5, 6, 21, 22, 23]:
            #     event._time = "NIGHT"
            # else:
            #     event._time = "DAY"
            CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
            CONTROLLER_ACTION[str(event)] = ctl_action4
    # EVENT - OWNER IN THE HOUSE
    elif (event.vs1 != ALERT and event.vs2 != ALERT) and event.dl == "":
        if event.vs1 != ALERT:
            event.vs1 = ""
        elif event.vs2 != ALERT:
            event.vs2 = ""

        event.fc1, event.fmd, event.dc, event.dl = "", "", "", ""
        event.bc1, event.bmd = "", ""

        # INTERNAL ACTIVITY
        if event.uss1:
            event.controller = "OWNER: ACTIVITY"

            # NIGHT
            if event._time in [0, 1, 2, 3, 4, 5, 6, 21, 22, 23]:
                # event._time = "NIGHT"
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ctl_action7
            else:
                # event._time = "DAY"
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ctl_action5
            print(event)
        else:  # NO INTERNAL ACTIVITY
            event.controller = "OWNER: NO_ACTIVITY"
            # NIGHT
            if event._time in [0, 1, 2, 3, 4, 5, 6, 21, 22, 23]:
                # event._time = "NIGHT"
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ctl_action8
            else:
                # event._time = "DAY"
                if event._time == 0:
                    event._time = 1
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ctl_action6
            print(event)
    else:
        event.controller = "NO_ACTION"
        CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
        CONTROLLER_ACTION[str(event)] = NO_ACTION
        print(event)
        # print("SEE for yourself", str(event))
    time.sleep(random.uniform(0.1, 0.3))


def visualize():
    print(CONTROLLER)
    print(CONTROLLER_ACTION)
    print()
    OWNER_NO_ACTIVITY, OWNER_NO_ACTIVITY_ACTION = {}, {}
    OWNER_ACTIVITY, OWNER_ACTIVITY_ACTION = {}, {}
    OWNER_ENTER, OWNER_ENTER_ACTION = {}, {}
    OWNER_LEAVE, OWNER_LEAVE_ACTION = {}, {}
    FRONT_BREAK_IN, FRONT_BREAK_IN_ACTION = {}, {}
    BACK_BREAK_IN, BACK_BREAK_IN_ACTION = {}, {}
    NO_ACT, NO_ACT_ACTION = {}, {}

    for k, v in CONTROLLER.items():
        b = json.dumps({ki: vi for ki, vi in eval(k).items() if vi})
        z = eval(k)
        if z.get("CONTROLLER") == "OWNER: NO_ACTIVITY":
            # print(b + " - " + str(CONTROLLER_ACTION[k]) + " - " + str(v))
            OWNER_NO_ACTIVITY[z.get("TIME")] = v
            OWNER_NO_ACTIVITY_ACTION[z.get("TIME")] = (v, b, CONTROLLER_ACTION.get(k))
        elif z.get("CONTROLLER") == "OWNER: ACTIVITY":
            OWNER_ACTIVITY[z.get("TIME")] = v
            OWNER_ACTIVITY_ACTION[z.get("TIME")] = (v, b, CONTROLLER_ACTION.get(k))
        elif z.get("CONTROLLER") == "OWNER_ENTER":
            OWNER_ENTER[z.get("TIME")] = v
            OWNER_ENTER_ACTION[z.get("TIME")] = (v, b, CONTROLLER_ACTION.get(k))
        elif z.get("CONTROLLER") == "OWNER_LEAVE":
            OWNER_LEAVE[z.get("TIME")] = v
            OWNER_LEAVE_ACTION[z.get("TIME")] = (v, b, CONTROLLER_ACTION.get(k))
        elif z.get("CONTROLLER") == "FRONT_BREAK_IN":
            FRONT_BREAK_IN[z.get("TIME")] = v
            FRONT_BREAK_IN_ACTION[z.get("TIME")] = (v, b, CONTROLLER_ACTION.get(k))
        elif z.get("CONTROLLER") == "BACK_BREAK_IN":
            BACK_BREAK_IN[z.get("TIME")] = v
            BACK_BREAK_IN_ACTION[z.get("TIME")] = (v, b, CONTROLLER_ACTION.get(k))
        elif z.get("CONTROLLER") == "NO_ACTION":
            NO_ACT[z.get("TIME")] = v
            NO_ACT_ACTION[z.get("TIME")] = (v, b, CONTROLLER_ACTION.get(k))

    # for i in range(1, 24):
    #     if not OWNER_NO_ACTIVITY.get(i):
    #         OWNER_NO_ACTIVITY[i] = None
    #     if not OWNER_ACTIVITY.get(i):
    #         OWNER_ACTIVITY[i] = None
    #     if not OWNER_ENTER.get(i):
    #         OWNER_ENTER[i] = None
    #     if not OWNER_LEAVE.get(i):
    #         OWNER_LEAVE[i] = None
    #     if not FRONT_BREAK_IN.get(i):
    #         FRONT_BREAK_IN[i] = None
    #     if not BACK_BREAK_IN.get(i):
    #         BACK_BREAK_IN[i] = None

    # OWNER_NO_ACTIVITY = collections.OrderedDict(sorted(OWNER_NO_ACTIVITY.items()))
    # OWNER_ACTIVITY = collections.OrderedDict(sorted(OWNER_ACTIVITY.items()))
    # OWNER_ENTER = collections.OrderedDict(sorted(OWNER_ENTER.items()))
    # OWNER_LEAVE = collections.OrderedDict(sorted(OWNER_LEAVE.items()))
    # FRONT_BREAK_IN = collections.OrderedDict(sorted(FRONT_BREAK_IN.items()))
    # BACK_BREAK_IN = collections.OrderedDict(sorted(BACK_BREAK_IN.items()))
    #
    # OWNER_NO_ACTIVITY_ACTION = collections.OrderedDict(sorted(OWNER_NO_ACTIVITY_ACTION.items()))
    # OWNER_ACTIVITY_ACTION = collections.OrderedDict(sorted(OWNER_ACTIVITY_ACTION.items()))
    # OWNER_ENTER_ACTION = collections.OrderedDict(sorted(OWNER_ENTER_ACTION.items()))
    # OWNER_LEAVE_ACTION = collections.OrderedDict(sorted(OWNER_LEAVE_ACTION.items()))
    # FRONT_BREAK_IN_ACTION = collections.OrderedDict(sorted(FRONT_BREAK_IN_ACTION.items()))
    # BACK_BREAK_IN_ACTION = collections.OrderedDict(sorted(BACK_BREAK_IN_ACTION.items()))

    for k, v in OWNER_ENTER_ACTION.items():
        print("Enter: ", k, v)

    for k, v in OWNER_LEAVE_ACTION.items():
        print("leave: ", k, v)

    for k, v in FRONT_BREAK_IN_ACTION.items():
        print("front break-in: ", k, v)

    for k, v in OWNER_ACTIVITY_ACTION.items():
        print("HO activity: ", k, v)

    for k, v in OWNER_NO_ACTIVITY_ACTION.items():
        print("HO no activity: ", k, v)

    for k, v in BACK_BREAK_IN_ACTION.items():
        print("back break-in: ", k, v)

    for k, v in NO_ACT_ACTION.items():
        print("No action: ", k, v)

    # print(OWNER_ENTER_ACTION)
    # print(OWNER_LEAVE_ACTION)
    # print(FRONT_BREAK_IN_ACTION)
    # print(OWNER_ACTIVITY_ACTION)
    # print(OWNER_NO_ACTIVITY_ACTION)
    # print(BACK_BREAK_IN_ACTION)
    # print(NO_ACT_ACTION)


    pd.options.plotting.backend = "plotly"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(OWNER_NO_ACTIVITY.keys()), y=list(OWNER_NO_ACTIVITY.values()),
                             name="OWNER NO_ACTIVITY",
                             mode="lines+markers", marker=dict(size=10, line=dict(width=1)),
                             ))
    fig.add_trace(go.Scatter(x=list(OWNER_ACTIVITY.keys()), y=list(OWNER_ACTIVITY.values()),
                             name="OWNER HOME ACTIVITY",
                             mode="lines+markers", marker=dict(size=10, line=dict(width=1)),
                             ))
    fig.add_trace(go.Scatter(x=list(OWNER_ENTER.keys()), y=list(OWNER_ENTER.values()),
                             name="OWNER ENTER HOUSE",
                             mode="lines+markers", marker=dict(size=10, line=dict(width=1)),
                             ))
    fig.add_trace(go.Scatter(x=list(OWNER_LEAVE.keys()), y=list(OWNER_LEAVE.values()),
                             name="OWNER LEAVE HOUSE",
                             mode="lines+markers", marker=dict(size=10, line=dict(width=1)),
                             ))
    fig.add_trace(go.Scatter(x=list(FRONT_BREAK_IN.keys()), y=list(FRONT_BREAK_IN.values()),
                             name="BREAK-IN EVENT IN FRONT",
                             mode="lines+markers", marker=dict(size=10, line=dict(width=1)),
                             ))
    fig.add_trace(go.Scatter(x=list(BACK_BREAK_IN.keys()), y=list(BACK_BREAK_IN.values()),
                             name="BREAK-IN EVENT IN BACK",
                             mode="lines+markers", marker=dict(size=10, line=dict(width=1)),
                             ))

    fig.update_xaxes(showgrid=True, ticks="outside")
    fig.update_layout(width=800, height=500,
                      title='Event occurrence and frequency in smart home for different scenarios',
                      xaxis_title='day time',
                      yaxis_title='counts')
    # fig.show()


if __name__ == '__main__':
    main()
    visualize()
