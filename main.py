from PySide6.QtWidgets import QApplication, QMenuBar,QMenu,QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QWidget, QTextEdit, QPushButton, QComboBox, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QIcon,QAction
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

        # 初始化波特率列表
        self.init_baud_rates()

        # 连接信号与槽
        
        self.com_combo.currentTextChanged.connect(self.update_com_name)
        self.baud_combo.currentTextChanged.connect(self.update_baud_name)
        # 设置窗口标题
        self.window.setWindowTitle("串口助手")
        self.window.setWindowIcon(QIcon("./resource/icon.png"))  # 设置窗口图标
        # 设置按钮图标

        # 定时器，用于读取串口数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)

        # 定时器，用于刷新可用串口
        self.port_refresh_timer = QTimer()
        self.port_refresh_timer.timeout.connect(self.update_available_ports)
        self.port_refresh_timer.start(1000)  # 每秒刷新一次可用串口
        self.show_img(img_path)  # 显示图片

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
            # 如果对象已被删除，捕获异常并停止定时器
            if hasattr(self, 'port_refresh_timer'):
                self.port_refresh_timer.stop()

    def update_com_name(self, text):
        # 将选中的端口号更新到 ComName
        self.com_name.setText(text)

    def update_baud_name(self, text):
        # 将选中的波特率更新到 BaudName
        self.bote_name.setText(text)

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

class Message(MainWindow):
    def __init__(self, ui_file):
        super().__init__(ui_file)
        self.message = self.central_widget.findChild(QTextEdit, "message")
        self.clear_button = self.central_widget.findChild(QPushButton, "clear")
        self.pause_button = self.central_widget.findChild(QPushButton, "pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        self.clear_button.clicked.connect(self.clear_message)
        self.start_button.clicked.connect(self.start_port)
        self.close_button.clicked.connect(self.close_port)
        self.clear_button.setIcon(QIcon(broom_icon_path))  # 清空按钮图标
        self.pause_button.setIcon(QIcon(pause_icon_path))  # 暂停按钮图标
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
    
class Plot(MainWindow):
    def __init__(self, ui_file):
        super().__init__(ui_file)

class Menu(QObject):
    def __init__(self, ui_file):
        super().__init__()
        loader = QUiLoader()
        self.window = loader.load(ui_file, None)
        if not self.window:
            print("UI 文件加载失败")
            sys.exit(1)
        self.window.setWindowTitle("串口助手")
        self.window.setWindowIcon(QIcon("./resource/icon.png"))
        
        # 创建 QStackedWidget
        self.stacked_widget = QStackedWidget()
        
        # 创建各界面实例
        self.Message_window = Message(Message_path)
        self.Plot_window = Plot(Plot_path)
        
        # 将界面添加到堆栈窗口
        self.stacked_widget.addWidget(self.Message_window.central_widget)
        self.stacked_widget.addWidget(self.Plot_window.central_widget)
        
        # 设置堆栈窗口为中心窗口
        self.window.setCentralWidget(self.stacked_widget)
        
        # 其余代码不变
        MenuBar = self.window.findChild(QMenuBar, "menubar")
        if not MenuBar:
            print("未找到菜单栏")
            sys.exit(1)
        MenuMessage = MenuBar.findChild(QMenu, "menuMessage")
        MenuPlot = MenuBar.findChild(QMenu, "menuPlot")
        message_action = QAction("消息界面", self)
        plot_action = QAction("绘图界面", self)
        
        # 将动作添加到已有菜单中
        MenuMessage.addAction(message_action)
        MenuPlot.addAction(plot_action)
        
        # 将动作与槽函数连接，用 setCentralWidget 切换界面
        message_action.triggered.connect(self.show_message_widget)
        plot_action.triggered.connect(self.show_plot_widget)
        
        # 只创建一个全局定时器来更新所有界面的端口列表
        self.port_refresh_timer = QTimer()
        self.port_refresh_timer.timeout.connect(self.update_all_ports)
        self.port_refresh_timer.start(1000)  # 每秒刷新一次
        
    def update_all_ports(self):
        """更新所有界面的端口列表"""
        try:
            # 获取当前可用的串口
            ports = [port.device for port in serial.tools.list_ports.comports()]
            
            # 更新 Message 界面的端口列表
            if hasattr(self.Message_window, 'com_combo'):
                current_ports = set(self.Message_window.com_combo.itemText(i) for i in range(self.Message_window.com_combo.count()))
                if set(ports) != current_ports:
                    self.Message_window.com_combo.clear()
                    self.Message_window.com_combo.addItems(ports)
            
            # 更新 Plot 界面的端口列表
            if hasattr(self.Plot_window, 'com_combo'):
                current_ports = set(self.Plot_window.com_combo.itemText(i) for i in range(self.Plot_window.com_combo.count()))
                if set(ports) != current_ports:
                    self.Plot_window.com_combo.clear()
                    self.Plot_window.com_combo.addItems(ports)
        except Exception as e:
            print(f"更新端口列表时出错: {e}")
            
    def show_message_widget(self):
        """显示消息界面"""
        self.stacked_widget.setCurrentIndex(0)  # 切换到第一个界面
        
    def show_plot_widget(self):
        """显示绘图界面"""
        self.stacked_widget.setCurrentIndex(1)  # 切换到第二个界面

if __name__ == "__main__":
    app = QApplication([])
    if getattr(sys, 'frozen', False):  # 如果是打包后的环境
        base_path = sys._MEIPASS
    else:  # 开发环境
        base_path = os.path.dirname(__file__)
        
    img_path = os.path.join(base_path, "resource", "img.png")
    ui_file = os.path.join(base_path, "Menu.ui")
    broom_icon_path = os.path.join(base_path, "resource", "broom.svg")
    pause_icon_path = os.path.join(base_path, "resource", "pause.svg")
    Message_path = os.path.join(base_path, "Message.ui")
    Plot_path = os.path.join(base_path, "Plot.ui")
    window = Menu(ui_file)
    window.window.resize(895, 630)
    window.window.show()

    sys.exit(app.exec())