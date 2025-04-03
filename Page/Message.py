from PySide6.QtWidgets import QTextEdit, QPushButton
import serial  # 第三方库 pyserial
from Page.MainWindow import MainWindow
from PySide6.QtCore import QTimer
class Message(MainWindow):
    def __init__(self, ui_file):
        super().__init__(ui_file)
        self.message = self.central_widget.findChild(QTextEdit, "message")
        self.clear_button = self.central_widget.findChild(QPushButton, "clear")
        self.pause_button = self.central_widget.findChild(QPushButton, "pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        self.clear_button.clicked.connect(self.clear_message)
        self.start_button.clicked.connect(self.start_port)
        self.close_button.clicked.connect(self.close_port) # 暂停按钮图标
        # 定时器，用于读取串口数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)
    def read_serial_data(self):
        # 读取串口数据
        if self.IsOpen and not self.IsPause:
            try:
                if self.serial_port.in_waiting > 0:  # 检查是否有数据可读
                    data = self.serial_port.readline().decode('utf-8').strip()
                    self.message.append(f"{data}")
            except Exception as e:
                self.message.append(f"读取数据失败：{str(e)}")
    def start_port(self):
        if self.IsOpen:
            self.message.append("端口已经打开")
            return
        # 获取端口号和波特率
        port = self.com_name.toPlainText().strip()
        baud_rate = self.bote_name.toPlainText().strip()

        if not port or not baud_rate:
            self.message.append("启动端口失败：端口号或波特率为空")
            return

        # 打开端口逻辑
        try:
            self.serial_port = serial.Serial(port, int(baud_rate), timeout=1)
            self.IsOpen = self.serial_port.is_open
            if self.IsOpen:
                self.message.append(f"启动端口成功：端口号={port}, 波特率={baud_rate}")
                self.timer.start(100)  # 每100毫秒检查一次串口数据
            else:
                self.message.append("启动端口失败")
        except Exception as e:
            self.message.append(f"启动端口失败：{str(e)}")

    def close_port(self):
        if not self.IsOpen:
            self.message.append("端口未打开")
            return
        # 关闭端口逻辑
        try:
            if self.serial_port:
                self.serial_port.close()
            self.IsOpen = False
            self.timer.stop()  # 停止定时器
            self.message.append("关闭端口成功")
        except Exception as e:
            self.message.append(f"关闭端口失败：{str(e)}")

    def toggle_pause(self):
        if not self.IsOpen:
            self.message.append("端口未打开，无法暂停")
            return
        self.IsPause = not self.IsPause  # 切换暂停状态
        state = "暂停" if self.IsPause else "继续"
        self.message.append(f"串口读取已{state}")

    def clear_message(self):
        # 清空消息框
        self.message.clear()