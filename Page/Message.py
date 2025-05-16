from PySide6.QtWidgets import QTextEdit, QPushButton
import serial  # 第三方库 pyserial
from Page.MainWindow import MainWindow
from PySide6.QtCore import QTimer
class Message(MainWindow):
    def __init__(self, ui_file):
        super().__init__(ui_file)
        self.message = self.central_widget.findChild(QTextEdit, "message")
        self.clear_button = self.central_widget.findChild(QPushButton, "clear")
        
        self.clear_button.clicked.connect(self.clear_message)
        self.start_button.clicked.connect(self.start_port)
        self.close_button.clicked.connect(self.close_port) # 暂停按钮图标
        # 定时器，用于读取串口数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)
    def read_serial_data(self):
        # 读取串口数据
        if MainWindow.IsOpen:
            try:
                if MainWindow.serial_port.in_waiting > 0:  # 检查是否有数据可读
                    data = MainWindow.serial_port.readline().decode('utf-8').strip()
                    self.message.append(f"{data}")
            except Exception as e:
                self.message.append(f"读取数据失败：{str(e)}")

    

    def clear_message(self):
        # 清空消息框
        self.message.clear()
    def start_port(self):
        MainWindow.start_mport(self)
        if MainWindow.IsOpen and self.central_widget.isVisible():
                # self.message.append(f"启动端口成功：端口号={port}, 波特率={baud_rate}")
                self.timer.start(3)  # 启动读取定时器
        else:
            self.message.append("启动端口失败")
    def close_port(self):
        MainWindow.close_mport(self)
        if MainWindow.IsOpen:
            self.timer.stop()