from PySide6.QtWidgets import QApplication, QMenuBar, QMenu, QStackedWidget, QWidget, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QObject, QTimer
import serial  # 第三方库 pyserial
import serial.tools.list_ports
import os
import sys
import shutil  # 添加用于复制文件
from Page.Plot import Plot
from Page.Message import Message
from Page.Login import Login
from Page.Learn import Learn

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
        self.learn_window = Learn(Learn_path)
        self.Message_window.clear_button.setIcon(QIcon(broom_icon_path))  # 清空按钮图标
        self.Message_window.pause_button.setIcon(QIcon(pause_icon_path)) 
        self.Message_window.show_img(img_path)  # 显示图片
        self.Plot_window.show_img(img_path)  # 显示图片
        self.learn_window.show_img(img_path)
        # 将界面添加到堆栈窗口
        self.stacked_widget.addWidget(self.Message_window.central_widget)
        self.stacked_widget.addWidget(self.Plot_window.central_widget)
        self.stacked_widget.addWidget(self.learn_window.central_widget)
        # 设置堆栈窗口为中心窗口
        self.window.setCentralWidget(self.stacked_widget)

        # 设置默认显示的界面为登录界面
        self.stacked_widget.setCurrentIndex(0)  # 默认显示登录界面
        
        # 获取菜单栏
        MenuBar = self.window.findChild(QMenuBar, "menubar")
        if not MenuBar:
            print("未找到菜单栏")
            sys.exit(1)
        # 获取其他菜单
        MenuMessage = MenuBar.findChild(QMenu, "menuMessage")
        MenuPlot = MenuBar.findChild(QMenu, "menuPlot")
        MenuLearn = MenuBar.findChild(QMenu, "menuLearn")
        MenuFile = MenuBar.findChild(QMenu, "menuFile")
        message_action = QAction("消息界面", self)
        plot_action = QAction("绘图界面", self)
        learn_actin = QAction("预测界面", self)
        File_action = QAction("打开", self)
        # 将动作添加到已有菜单中
        MenuMessage.addAction(message_action)
        MenuPlot.addAction(plot_action)
        MenuLearn.addAction(learn_actin)
        MenuFile.addAction(File_action)
        # 将动作与槽函数连接，用 setCentralWidget 切换界面
        message_action.triggered.connect(self.show_message_widget)
        plot_action.triggered.connect(self.show_plot_widget)
        learn_actin.triggered.connect(self.show_learn_widget)
        File_action.triggered.connect(self.open_model_file)
        # 只创建一个全局定时器来更新所有界面的端口列表
        self.port_refresh_timer = QTimer()
        self.port_refresh_timer.timeout.connect(self.update_all_ports)
        self.port_refresh_timer.start(1000)  # 每秒刷新一次

    def open_model_file(self):
        """打开模型文件并替换model目录中的transformer.pt文件"""
        try:
            # 获取可执行文件或脚本所在的基本路径
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            # 打开文件对话框，只显示.pt文件
            file_path, _ = QFileDialog.getOpenFileName(
                self.window,
                "选择模型文件",
                "",
                "PyTorch模型文件 (*.pt)"
            )
            
            if file_path:
                # 确保model目录存在
                model_dir = os.path.join(base_path, "model")
                if not os.path.exists(model_dir):
                    os.makedirs(model_dir)
                
                # 目标文件路径
                target_file = os.path.join(model_dir, "transformer.pt")
                
                # 复制选择的文件到目标位置（会覆盖现有文件）
                shutil.copy2(file_path, target_file)
                
                # 通知用户文件已成功替换
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self.window,
                    "成功",
                    f"模型文件已成功更新到：\n{target_file}"
                )
                
                # # 如果当前显示的是学习界面，可以在这里刷新模型（可选）
                # if self.stacked_widget.currentIndex() == 2:
                #     # 可以在这里添加刷新模型的代码，或提示用户重启应用
                #     pass
                    
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self.window,
                "错误",
                f"更新模型文件时出错：{str(e)}"
            )

    # 更新端口等现有方法保持不变
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
        
    def show_learn_widget(self):
        self.stacked_widget.setCurrentIndex(2)  # 切换到第三个界面

if __name__ == "__main__":
    app = QApplication([])
    if getattr(sys, 'frozen', False):  # 如果是打包后的环境
        base_path = sys._MEIPASS
    else:  # 开发环境
        base_path = os.path.dirname(__file__)
    # 获取相关资源
    img_path = os.path.join(base_path, "resource", "img.png")
    login_path = os.path.join(base_path, "resource", "login.jpg")
    ui_file = os.path.join(base_path, "Menu.ui")
    user_path = os.path.join(base_path, "userinfo.csv")
    broom_icon_path = os.path.join(base_path, "resource", "broom.svg")
    pause_icon_path = os.path.join(base_path, "resource", "pause.svg")
    Message_path = os.path.join(base_path, "Message.ui")
    Plot_path = os.path.join(base_path, "Plot.ui")
    Login_path = os.path.join(base_path, "Login.ui")
    Learn_path = os.path.join(base_path, "Learn.ui")
    # 显示登录界面
    login_window = Login(Login_path,user_path)
    login_window.show_img(login_path)  # 显示图片
    login_window.window.show()
    
    # 登录成功后显示主界面
    def on_login_success():
        global main_window  # 定义为全局变量
        main_window = Menu(ui_file)
        main_window.window.resize(895, 630)
        main_window.window.show()
        login_window.window.close()  # 关闭登录界面

    login_window.login_success.connect(on_login_success)
    # window = Menu(ui_file)
    # window.window.resize(895, 630)
    # window.stacked_widget.setCurrentIndex(0)  # 默认显示登录界面
    # window.window.show()
  
    sys.exit(app.exec())

