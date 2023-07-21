import json
import random
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#
#
# data = {
#     "block_data":
#         {
#             "amount": "0",
#             "data": "test data",
#             "recipient": "2",
#             "sender": "1"
#         }
# }


class Event:
    def __init__(self, front_camera1, back_camera1, door_camera, door_lock, rfid1, sw1):
        self.front_camera1 = front_camera1
        self.back_camera1 = back_camera1
        self.door_camera = door_camera
        self.door_lock = door_lock
        self.rfid1 = rfid1
        self.sw1 = sw1
        self.controller = None

    def __str__(self):
        d = {
            "FC1": self.front_camera1,
            "BC1": self.back_camera1,
            "DC": self.door_camera,
            "DL": self.door_lock,
            "RFID": self.rfid1,
            "SW": self.sw1
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
    BACK_CAMERA1 = ["PASS", "ALERT", ""]
    # BACK_CAMERA1 = [""]
    DOOR_CAMERA = ["PASS", "ALERT", ""]
    DOOR_LOCK = ["PASS", "ALERT", ""]
    RFID1 = ["ALERT", ""]
    # RFID1 = [""]
    SW1 = ["ALERT", ""]

    CONTROLLER = {}
    CONTROLLER_ACTION = {}
    ALERT = "ALERT"
    NO_ACTION = "NO ACTION"

    for i in range(50):
        front_camera1, back_camera1, door_camera, door_lock, rfid1, sw1 = \
            random.choice(FRONT_CAMERA1), random.choice(BACK_CAMERA1), random.choice(
                DOOR_CAMERA), random.choice(DOOR_LOCK), random.choice(RFID1), random.choice(SW1)
        event = Event(front_camera1, back_camera1, door_camera, door_lock, rfid1, sw1)

        if event.front_camera1 == ALERT:
            if event.door_camera == ALERT or event.door_lock == ALERT and event.sw1 == ALERT:
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ALERT
            elif event.rfid1 == ALERT and event.sw1 == ALERT:
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ALERT

        elif event.back_camera1 == ALERT:
            if event.rfid1 == ALERT or (event.rfid1 == ALERT and event.sw1 == ALERT):
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ALERT
            elif not event.front_camera1 == ALERT and not event.door_camera == ALERT and \
                    not event.door_lock == ALERT:
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = NO_ACTION
            elif not event.rfid1 == ALERT and not event.sw1 == ALERT:
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = NO_ACTION

        elif event.door_camera == ALERT:
            if (event.door_lock == ALERT and event.sw1 == ALERT) or \
                    (not event.door_lock == ALERT and event.sw1 == ALERT) or \
                    event.door_lock == ALERT or event.rfid1 == ALERT or \
                    (event.rfid1 == ALERT and event.sw1 == ALERT):
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ALERT

        elif event.door_lock == ALERT:
            if event.rfid1 == ALERT or (event.rfid1 == ALERT and event.sw1 == ALERT) \
                    or event.sw1 == ALERT:
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ALERT

        elif event.rfid1 == ALERT and event.sw1 == ALERT:
            if not event.front_camera1 == ALERT and not event.door_camera == ALERT and \
                    not event.door_lock == ALERT and not event.back_camera1 == ALERT:
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ALERT

        elif event.front_camera1 == "PASS":
            if (event.door_camera == ALERT and event.door_lock == ALERT) or \
                    (event.door_camera == ALERT and event.sw1 == ALERT) or \
                    (event.door_lock == ALERT and event.sw1 == ALERT) or \
                    (event.rfid1 == ALERT and event.sw1 == ALERT):
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ALERT
            elif event.door_camera == "PASS" and event.door_lock == "PASS" and \
                    not event.rfid1 == ALERT:
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = NO_ACTION

        elif event.front_camera1 == "" and event.door_camera == "PASS" and \
                event.door_lock == "PASS" and not event.rfid1 == ALERT:
            CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
            CONTROLLER_ACTION[str(event)] = NO_ACTION

        elif event.back_camera1 == "PASS":
            if event.door_camera == "PASS" or event.door_lock == "PASS":
                CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
                CONTROLLER_ACTION[str(event)] = ALERT
        else:

            CONTROLLER[str(event)] = CONTROLLER.setdefault(str(event), 0) + 1
            CONTROLLER_ACTION[str(event)] = "SEE for yourself"
            print("SEE for yourself", str(event))

    # for k, v in CONTROLLER.items():
    #     if CONTROLLER_ACTION[k] == NO_ACTION:
    #         print(k, v)
    #         print(CONTROLLER_ACTION[k])
    # print(CONTROLLER)
    # print(CONTROLLER_ACTION)
    return CONTROLLER, CONTROLLER_ACTION


def visualize(CONTROLLER, CONTROLLER_ACTION):
    import pandas as pd
    ALERT = {}
    NO_ALERT = {}
    # ENEMY = []
    MMMM = []
    x_alert = []
    y_alert = []
    x_no_alert = []
    y_no_alert = []
    i, j = 1, 1
    for k, v in CONTROLLER.items():
        a = eval(k)
        b = json.dumps({ki: vi for ki, vi in eval(k).items() if vi})
        if CONTROLLER_ACTION[k] == "ALERT":
            # print(b, v)
            name1 = "Event"+str(i)
            ALERT[name1] = b
            i += 1
            x_alert.append(name1)
            y_alert.append(v)
            # ALERT[b] = v
        elif CONTROLLER_ACTION[k] == "NO ACTION":
            # print(b, v)
            name2 = "Event" + str(j)
            NO_ALERT[name2] = b
            j += 1
            x_no_alert.append(name2)
            y_no_alert.append(v)
            # NO_ALERT[b] = v

    for k, v in ALERT.items():
        print(k + ": " + v)
    print()
    for k, v in NO_ALERT.items():
        print(k + ": " + v)


    pd.options.plotting.backend = "plotly"
    # fig1 = go.Bar(x=x_alert, y=y_alert, base={
    #                  "x": "Events captured",
    #                  "y": "Counts"
    #              }, name='Controller - Alerted user')
    #
    # # title = "Controller - Alert action for the number of events captured"
    #
    # fig2 = go.Bar(x=x_no_alert, y=y_no_alert, base={
    #     "x": "Events captured",
    #     "y": "Counts"
    # }, name='Controller - No action taken', text="ABC")
    # # title = "Controller - NO Action taken for the number of events captured"
    #
    # fig = make_subplots(rows=1, cols=2)
    # fig.add_trace(fig1, row=1, col=1)
    # fig.add_trace(fig2, row=1, col=2)
    #
    # fig.update_xaxes(showgrid=True, ticks="outside")
    # fig.update_layout(title='A Controller action graph - barchart representing the number of '
    #                         'events captured')
    # fig.show()


    # fig = px.bar(x=x_alert, y=y_alert, labels={
    #     "x": "Events captured",
    #     "y": "Events Counts"
    # }, width=1200, height=800, color=ALERT, title="Controller - User alerted for the captured "
    #                                              "events")
    #
    # fig.update_xaxes(showgrid=True, ticks="outside")
    # fig.show()
    #
    # fig2 = px.bar(x=x_no_alert, y=y_no_alert, labels={
    #     "x": "Events captured",
    #     "y": "Events Counts"
    # }, width=800, height=400, color=NO_ALERT, title="Controller - No action for the captured "
    #                                                 "events")
    #
    # fig2.update_xaxes(showgrid=True, ticks="outside")
    # fig2.show()


    # no action


if __name__ == '__main__':
    CONTROLLER, CONTROLLER_ACTION = main()
    visualize(CONTROLLER, CONTROLLER_ACTION)
