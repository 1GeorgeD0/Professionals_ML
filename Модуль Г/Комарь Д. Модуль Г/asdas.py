#Импортирование библиотек
import requests
import PySimpleGUI as sg


#объвление полей в программе
layout = [[sg.Text('Ссылка на сайт'), sg.InputText()],
    [sg.Output(size=(88, 20))],
    [sg.Button('Запуск',enable_events=True, key = 'b1')]]
window = sg.Window('Номинация  премии Рунета', layout)



#Цикл работы программы
while True:                            
    event, values = window.read()
    if event in (None,'Exit'):
        break
    if event in ('b1'):
        try:
            if (str(requests.get(str(values[0]))) == "<Response [200]>"):
                print("Сайт доступен")
            else:
                print("Сайт не доступен")
        except Exception: 
            print("Ошибка ввода")
window.close()