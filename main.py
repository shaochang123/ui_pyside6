from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QWidget, QTextEdit, QPushButton, QComboBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QObject, QTimer
import serial  # 第三方库 pyserial
import serial.tools.list_ports
import os
import sys

class MainWindow(QObject):
    def __init__(self, ui_file):
        super().__init__()
        # 加载UI文件
        loader = QUiLoader()
        self.window = loader.load(ui_file, None)
        self.IsOpen = False
        self.IsPause = False  # 暂停状态
        self.serial_port = None  # 串口对象
        if not self.window:
            print("UI 文件加载失败")
            sys.exit(1)

        # 获取 centralWidget
        central_widget = self.window.findChild(QWidget, "centralwidget")
        if not central_widget:
            print("未找到 centralWidget")
            sys.exit(1)

        # 获取组件
        self.com_name = central_widget.findChild(QTextEdit, "ComName")
        self.bote_name = central_widget.findChild(QTextEdit, "BaudName")
        self.message = central_widget.findChild(QTextEdit, "message")
        self.start_button = central_widget.findChild(QPushButton, "start")
        self.clear_button = central_widget.findChild(QPushButton, "clear")
        self.close_button = central_widget.findChild(QPushButton, "close")
        self.pause_button = central_widget.findChild(QPushButton, "pause")
        self.img_view = central_widget.findChild(QGraphicsView, "image")  # 获取 QGraphicsView
        self.com_combo = central_widget.findChild(QComboBox, "com_combo")  # 获取端口 ComboBox
        self.baud_combo = central_widget.findChild(QComboBox, "baud_combo")  # 获取波特率 ComboBox

        if not all([self.com_name, self.bote_name, self.message, self.start_button, self.clear_button, self.close_button, self.img_view, self.com_combo, self.baud_combo]):
            print("未找到必要的组件")
            sys.exit(1)

        # 初始化波特率列表
        self.init_baud_rates()

        # 连接信号与槽
        self.start_button.clicked.connect(self.start_port)
        self.clear_button.clicked.connect(self.clear_message)
        self.close_button.clicked.connect(self.close_port)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.com_combo.currentTextChanged.connect(self.update_com_name)
        self.baud_combo.currentTextChanged.connect(self.update_baud_name)

        # 设置窗口标题
        self.window.setWindowTitle("项目UI界面")

        # 设置按钮图标
        self.clear_button.setIcon(QIcon(broom_icon_path))  # 清空按钮图标
        self.pause_button.setIcon(QIcon(pause_icon_path))  # 暂停按钮图标

        # 定时器，用于读取串口数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)

        # 定时器，用于刷新可用串口
        self.port_refresh_timer = QTimer()
        self.port_refresh_timer.timeout.connect(self.update_available_ports)
        self.port_refresh_timer.start(1000)  # 每秒刷新一次可用串口

    def init_baud_rates(self):
        # 常用波特率
        baud_rates = ["9600", "19200", "38400", "57600", "115200"]
        self.baud_combo.addItems(baud_rates)

    def update_available_ports(self):
        # 获取当前可用的串口
        ports = [port.device for port in serial.tools.list_ports.comports()]
        current_ports = set(self.port_combo.itemText(i) for i in range(self.port_combo.count()))

        # 更新 ComboBox 中的端口列表
        if set(ports) != current_ports:
            self.port_combo.clear()
            self.port_combo.addItems(ports)

    def update_com_name(self, text):
        # 将选中的端口号更新到 ComName
        self.com_name.setText(text)

    def update_baud_name(self, text):
        # 将选中的波特率更新到 BaudName
        self.bote_name.setText(text)

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

    def read_serial_data(self):
        # 读取串口数据
        if self.IsOpen and not self.IsPause:
            try:
                if self.serial_port.in_waiting > 0:  # 检查是否有数据可读
                    data = self.serial_port.readline().decode('utf-8').strip()
                    self.message.append(f"{data}")
            except Exception as e:
                self.message.append(f"读取数据失败：{str(e)}")

    def show_img(self,img_path):
        if not os.path.exists(img_path):
            self.message.append(f"图片文件不存在: {img_path}")
            return
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            self.message.append("图片加载失败，请检查图片格式或路径")
            return

        # 创建场景并加载图片
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)
        self.img_view.setScene(scene)  # 将场景设置到 QGraphicsView

if __name__ == "__main__":
    app = QApplication([])
    if getattr(sys, 'frozen', False):  # 如果是打包后的环境
        base_path = sys._MEIPASS
    else:  # 开发环境
        base_path = os.path.dirname(__file__)
        
    img_path = os.path.join(base_path, "resource", "img.png")
    ui_file = os.path.join(base_path, "main.ui")
    broom_icon_path = os.path.join(base_path, "resource", "broom.svg")
    pause_icon_path = os.path.join(base_path, "resource", "pause.svg")


    main_window = MainWindow(ui_file)
    main_window.show_img(img_path)  # 显示图片
    main_window.window.show()
    sys.exit(app.exec())