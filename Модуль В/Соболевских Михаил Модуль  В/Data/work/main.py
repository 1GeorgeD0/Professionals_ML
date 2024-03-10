import sys
from datetime import datetime                                             # +++
import json
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.autofmt_xdate()                                               # +++
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, x_list, y_list, *args, **kwargs):                  # + x_list, y_list
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
#        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        sc.axes.plot(x_list, y_list)                                      # + x_list, y_list

        self.setCentralWidget(sc)

# +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
_dict = {
    "status":"ok",
    "name":"Market Price (USD)",
    "unit":"USD",
    "period":"day",
    "description":"Average USD market price across major bitcoin exchanges.",
    "values":[
        {"x":1613088000, "y":48013.38},
        {"x":1613174400, "y":47471.4},
        {"x":1613260800, "y":47185.19},
        {"x":1613347200, "y":48720.37},
        {"x":1613433600, "y":47951.85},
        {"x":1613520000, "y":49160.1},
        {"x":1613606400, "y":52118.23},
        {"x":1613692800, "y":51608.15},
        {"x":1613779200, "y":55916.5},
        {"x":1613865600, "y":56001.2},
        {"x":1613952000, "y":57487.86},
        {"x":1614038400, "y":54123.4},
        {"x":1614124800, "y":48880.43},
        {"x":1614211200, "y":50624.84},
        {"x":1614297600, "y":46800.42},
        {"x":1614384000, "y":46340.31},
        {"x":1614470400, "y":46155.87},
        {"x":1614556800, "y":45113.92},
        {"x":1614643200, "y":49618.43},
        {"x":1614729600, "y":48356.04},
        {"x":1614816000, "y":50477.7},
        {"x":1614902400, "y":48448.91},
        {"x":1614988800, "y":48861.38},
        {"x":1615075200, "y":48881.59},
        {"x":1615161600, "y":51169.7},
        {"x":1615248000, "y":52299.33},
        {"x":1615334400, "y":54881.52},
        {"x":1615420800, "y":55997.23},
        {"x":1615507200, "y":57764},
        {"x":1615593600, "y":57253.28},
        {"x":1615680000, "y":61258.73}
    ]
}

x_list = []
y_list = []
for item in _dict["values"]:
    x_list.append(datetime.utcfromtimestamp(item['x']))
    y_list.append(item['y'])
#print(*x_list, sep='\n')
# +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(x_list, y_list)                                        # + x_list, y_list
    w.show()
    sys.exit(app.exec_())