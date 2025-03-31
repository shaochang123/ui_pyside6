from PySide6.QtWidgets import QApplication, QMenuBar,QMenu,QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon,QAction
from PySide6.QtCore import QObject, QTimer
import serial  # 第三方库 pyserial
import serial.tools.list_ports
import os
import sys
from Page.Plot import Plot
from Page.Message import Message
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
        self.Message_window.clear_button.setIcon(QIcon(broom_icon_path))  # 清空按钮图标
        self.Message_window.pause_button.setIcon(QIcon(pause_icon_path)) 
        self.Message_window.show_img(img_path)  # 显示图片
        self.Plot_window.show_img(img_path)  # 显示图片
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
    # 获取相关资源
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