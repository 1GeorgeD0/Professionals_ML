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

# "Наука, технологии и инновации" - 1
# "Государство и Общество" - 2 
# "Культурные проекты в сети" - 3  
# "Народов много - Родина одна" - 4 
# "Туризм и индустрия гостеприимства - 5 
# "Образование и Кадры" - 6
# "Экономика и Бизнес" - 7 
# "Подкасты и цифровой контент" - 8
# "Здоровье и медицина" - 9



_dict = (
[
     {"Альфа-Банк": 1},
     {"ВТБ": 2},
     {"Вконтакте": 3},
     {"Стрит-арт проект VK на день флага России. Агентство Wonder": 4},
     {"Авито": 5},
     {"Авито": 1},
     {"Лаборатория Касперского": 1},
     {"Росатом": 1},
     {"Место встречи VK": 1},
     {"Университет ИТМО и Napoleon IT": 6},
     {"Финуслуги": 7},
     {"Московский Кредитный Банк": 7},
     {"СберМаркет": 7}, 
     {"СберМаркет": 8},
     {"Тензор": 7},
     {"Проект по использованию технологий компьютерного зрения на базе искусственного интеллекта (ИИ) для анализа медицинских изображений": 9},
     {"Здоровье.ру": 9},
     {"Skillbox": 1},
     {"Gett": 1},
     {"Промобот": 1},
     {"Иннотех": 1},
     {"Ростелеком": 1, }
    ]
    [
     {"Альфа-Банк": 192.63},
     {"ВТБ": 143.74},
     {"Вконтакте": 907.2},
     {"Стрит-арт проект VK на день флага России. Агентство Wonder": 907.2},
     {"Авито": 192.85},
     {"Лаборатория Касперского": 331.1},
     {"Росатом": 35.46},
     {"Место встречи VK": 907.2},
     {"Университет ИТМО и Napoleon IT": 102.28},
     {"Финуслуги": 103.23},
     {"Московский Кредитный Банк": 41.41},
     {"СберМаркет": 115.98},
     {"Тензор": 76.07},
     {"Проект по использованию технологий компьютерного зрения на базе искусственного интеллекта (ИИ) для анализа медицинских изображений": 0},
     {"Здоровье.ру": 110},
     {"Skillbox": 118.13},
     {"Gett": 135.29},
     {"Промобот": 23},
     {"Иннотех": 47.73},
     {"Ростелеком": 107.51}
     ]
)

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