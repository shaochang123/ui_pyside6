from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QWidget, QTextEdit, QPushButton, QComboBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QObject, QTimer
import serial  # 第三方库 pyserial
import serial.tools.list_ports
import os
import sys
class MainWindow(QObject):
    # 添加静态变量用于跨界面共享
    serial_port = None
    
    IsOpen = False
    current_port = ""
    current_baud = ""
    
    def __init__(self, ui_file):
        super().__init__()
        # 加载UI文件
        loader = QUiLoader()
        self.window = loader.load(ui_file, None)
        if not self.window:
            print("UI 文件加载失败")
            sys.exit(1)

        # 获取 centralWidget
        central_widget = self.window.findChild(QWidget, "centralwidget")
        if not central_widget:
            print("未找到 centralWidget")
            sys.exit(1)

        self.central_widget = central_widget  # 把 central_widget 存到 self.central_widget

        # 获取组件
        
        self.com_name = central_widget.findChild(QTextEdit, "ComName")
        self.bote_name = central_widget.findChild(QTextEdit, "BaudName")
        self.start_button = central_widget.findChild(QPushButton, "start")
        self.close_button = central_widget.findChild(QPushButton, "close")
        self.img_view = central_widget.findChild(QGraphicsView, "image")  # 获取 QGraphicsView
        self.com_combo = central_widget.findChild(QComboBox, "port_combo")  # 获取端口 ComboBox
        self.baud_combo = central_widget.findChild(QComboBox, "baud_combo")  # 获取波特率 ComboBox
        if not all([self.com_name, self.bote_name,self.start_button,self.close_button, self.img_view, self.com_combo, self.baud_combo]):
            print("未找到必要的组件")
            sys.exit(1)
        # 连接信号与槽

        self.com_combo.activated.connect(self.update_com_name)
        self.baud_combo.activated.connect(self.update_baud_name)
        # 初始化波特率列表
        self.init_baud_rates()
        # 设置窗口标题
        self.window.setWindowTitle("串口助手")
        self.window.setWindowIcon(QIcon("./resource/icon.png"))  # 设置窗口图标
        # 设置按钮图标

        

        # 定时器，用于刷新可用串口
        self.port_refresh_timer = QTimer()
        self.port_refresh_timer.timeout.connect(self.update_available_ports)
        self.port_refresh_timer.start(3000)  # 每秒刷新一次可用串口

    def init_baud_rates(self):
        # 常用波特率
        baud_rates = ["9600", "19200", "38400", "57600", "115200"]
        self.baud_combo.addItems(baud_rates)

    def update_available_ports(self):
        # 安全检查：确保组件存在且有效
        if not hasattr(self, 'com_combo'):
            return
          
        try:
            # 获取当前可用的串口
            ports = [port.device for port in serial.tools.list_ports.comports()]
            # 修正：使用同一个组件的 count 和 itemText
            current_ports = set(self.com_combo.itemText(i) for i in range(self.com_combo.count()))

            # 更新 ComboBox 中的端口列表
            if set(ports) != current_ports:
                self.com_combo.clear()
                self.com_combo.addItems(ports)
        except RuntimeError:
            print("error")

    def update_com_name(self, idx):
        # 将选中的端口号更新到 ComName
        text = self.com_combo.itemText(idx)
        self.com_name.setText(text)  # 使用 setPlainText 而不是 setText
        MainWindow.current_port = text

    def update_baud_name(self, idx):
        # 将选中的波特率更新到 BaudName
        text = self.baud_combo.itemText(idx)
        self.bote_name.setText(text)
        MainWindow.current_baud = text

    def show_img(self,img_path):
        if not os.path.exists(img_path):
            print(f"图片文件不存在: {img_path}")
            return
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print("图片加载失败，请检查图片格式或路径")
            return

        # 创建场景并加载图片
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)
        self.img_view.setScene(scene)  # 将场景设置到 QGraphicsView

    def start_mport(self):
        # 检查全局状态而非实例状态
        if MainWindow.IsOpen:
            # self.message.append(f"端口已被打开：{MainWindow.current_port}，波特率：{MainWindow.current_baud}")
            # 同步本地状态
            return
            
        port = self.com_name.toPlainText().strip()
        baud_rate = self.bote_name.toPlainText().strip()

        if not port or not baud_rate:
            # self.message.append("启动端口失败：端口号或波特率为空")
            return

        try:
            # 更新全局静态变量
            MainWindow.serial_port = serial.Serial(port, int(baud_rate), timeout=1)
            MainWindow.IsOpen= MainWindow.serial_port.is_open
            MainWindow.current_port = port
            MainWindow.current_baud = baud_rate
        except Exception as e:
            print(f"启动端口失败：{str(e)}")

    def close_mport(self):
        if not MainWindow.IsOpen:
            # self.message.append("端口未打开")
            return
            
        try:
            if MainWindow.serial_port:
                MainWindow.serial_port.close()
                
            # 更新全局状态    
            MainWindow.IsOpen = False
            MainWindow.serial_port = None
        except Exception as e:
            print(f"关闭端口失败：{str(e)}")