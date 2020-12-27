import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
import os
import subprocess


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.setStyleSheet('QPushButton {background-color: green}')
        self.pushButton.setText('Старт системы')
        self.pushButton_2.setStyleSheet('QPushButton {background-color: blue}')
        self.pushButton_2.setText('Обновить')
        self.pushButton_3.setStyleSheet('QPushButton {background-color: orange}')
        self.pushButton_3.setText('Запуск сценариев')
        self.pushButton.clicked.connect(self.start_tcp)
        self.pushButton_2.clicked.connect(self.update)
        self.pushButton_3.clicked.connect(self.prog_func)
        self.listWidget.itemClicked.connect(self.data_module)

    def start_apps(self) -> None:
        my_dir = '/home/roman/lrs_protocol/module_information'
        files = os.listdir(my_dir)
        # for f in files:
        # if f.endswith(".txt"):
        #    os.remove(os.path.join(my_dir, f))

    # Delete all files .txt with module data  for cleaning
    def data_module(self) -> None:
        self.listWidget_3.clear()
        a = self.listWidget.currentItem().text()
        with open('/home/roman/lrs_protocol/module_information/' +
                  a[9:11] + '.txt', 'r') as file:
            self.listWidget_3.addItems((list(list(file))))

    def update(self) -> None:
        types = {'C': 'Camera module',
                 'V': 'Vehicle module',
                 'S': 'Science instruments',
                 'D': 'Spot micro',
                 'L': 'Claw',
                 'F': 'Flying module'}
        self.listWidget.clear()
        with open('/home/roman/lrs_protocol/ip_type.txt', 'r') as file:
            ip_types = list(file)
            for i in ip_types:
                self.listWidget.addItem(i[:-2] + str(types[str(i[-2:-1])]))

    def start_tcp(self) -> None:
        if self.pushButton.palette().button().color().name() == '#008000':
            self.pushButton.setStyleSheet('QPushButton {background-color: red}')
            self.pushButton.setText('Стоп системы')
            self.start_apps()
            subprocess.Popen([sys.executable, '/home/roman/lrs_protocol/server_tcp.py'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        elif self.pushButton.palette().button().color().name() == '#ff0000':
            os.system('pkill -f server_tcp.py')
            self.pushButton.setStyleSheet('QPushButton {background-color: green}')
            self.pushButton.setText('Старт системы')

    def ch_prog(self):
        prog = self.listWidget_2.currentItem().text()
        if str(prog[:-1]) == 'PM':
            print(1)
            os.system('sshpass -p raspberry ssh pi@10.42.43.17 python3 /home/pi/projects/PM/PM.py')
        elif str(prog[:-1]) == 'OCN':
            print(1)
            os.system('sshpass -p raspberry ssh pi@10.42.43.17 python3 /home/pi/projects/OCN/OCN.py')
        elif str(prog[:-1]) == 'SDC':
            os.system('sshpass -p raspberry ssh pi@10.42.43.11 python3 /home/pi/projects/SDC/SDC.py')
        elif str(prog[:-1]) == 'SCB':
            os.system(
                'sshpass -p raspberry ssh pi@10.42.43.15 python3 /home/pi/projects/SCB/SCB.py --ip 0.0.0.0 --port 8000')
        elif str(prog[:-1]) == 'DPR':
            print(1)
            os.system(
                'sshpass -p raspberry ssh pi@10.42.43.15 python3 /home/pi/projects/DPR/pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings /home/pi/projects/DPR/encodings.pickle --ip 0.0.0.0 --port 8000')

    def prog_func(self):
        ssh_directory = '/home/pi/projects/'
        commands_file = '/home/roman/lrs_protocol/commands.txt'
        ip_type_file = '/home/roman/lrs_protocol/ip_type.txt'
        problem_with_program = []

        color_3 = self.pushButton_3.palette().button().color()
        if color_3.name() == '#ffa500':
            with open('/home/roman/lrs_protocol/commands.txt', 'r') as file:
                commands = list(file)
                for i in commands:
                    self.listWidget_2.addItem(i)
            self.listWidget_2.itemClicked.connect(self.ch_prog)

            # subprocess.Popen([sys.executable, '/home/roman/lrs_protocol/server_tcp.py'],
            #                 stdout=subprocess.PIPE,
            #                stderr=subprocess.STDOUT)
        else:
            self.pushButton_3.setStyleSheet('QPushButton {background-color: orange}')
            self.pushButton_3.setText('Запуск сценариев')
            print('[LOG] Exit from current programs')


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()
