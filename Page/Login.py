from PySide6.QtWidgets import QWidget, QMessageBox, QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtUiTools import QUiLoader
import os
from utils.utils import save_user_info, get_user_info
from utils.share import shareInfo


class Login(QWidget):
    login_success = Signal()  # 定义登录成功信号

    def __init__(self, ui_file):
        super().__init__()
        loader = QUiLoader()
        self.window = loader.load(ui_file, None)
        if not self.window:
            print("UI 文件加载失败")
            return
        


        # 隐藏窗口边框
        self.window.setWindowFlags(Qt.FramelessWindowHint)
        self.window.setAttribute(Qt.WA_TranslucentBackground)

        # 初始化控件
        self.init_ui()
        self.init_slot()

    def init_ui(self):
        """初始化控件"""
        self.stacked_widget = self.window.findChild(QWidget, "stackedWidget")
        self.username_input = self.window.findChild(QLineEdit, "lineEdit_6")
        self.password_input = self.window.findChild(QLineEdit, "lineEdit_7")
        self.new_username_input = self.window.findChild(QLineEdit, "lineEdit_3")
        self.new_password_input = self.window.findChild(QLineEdit, "lineEdit_4")
        self.confirm_password_input = self.window.findChild(QLineEdit, "lineEdit_5")

        # 设置密码输入框为隐藏模式
        self.password_input.setEchoMode(QLineEdit.Password)

    def init_slot(self):
        """初始化信号槽"""
        # 登录按钮
        self.window.findChild(QWidget, "login_1").clicked.connect(self.sign_in)
        # 注册按钮
        self.window.findChild(QWidget, "register_1").clicked.connect(self.new_account)
        # 切换到登录界面
        self.window.findChild(QWidget, "login_0").clicked.connect(lambda: self.goto_stack(0))
        # 切换到注册界面
        self.window.findChild(QWidget, "register_0").clicked.connect(lambda: self.goto_stack(1))
        # 取消按钮
        self.window.findChild(QWidget, "cancel_1").clicked.connect(lambda: self.goto_stack(0))

    def sign_in(self):
        """登录逻辑"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # 获取已注册用户信息
        USERS = get_user_info()
        if username not in USERS.keys():
            QMessageBox.warning(self.window, '!', '用户不存在', QMessageBox.Yes)
            self.goto_stack(0)
        else:
            if USERS.get(username) == password:
                # 登录成功，发送信号
                self.login_success.emit()
                self.window.close()
            else:
                QMessageBox.warning(self.window, '!', '密码输入错误', QMessageBox.Yes)
                self.goto_stack(0)

    def new_account(self):
        """注册逻辑"""
        USERS = get_user_info()
        new_username = self.new_username_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if new_username == "":
            QMessageBox.warning(self.window, '!', '账号名不许为空', QMessageBox.Yes)
        elif new_username in USERS.keys():
            QMessageBox.warning(self.window, '!', '账号已存在', QMessageBox.Yes)
            self.goto_stack(1)
        elif new_password != confirm_password:
            QMessageBox.warning(self.window, '!', '密码不一致', QMessageBox.Yes)
            self.goto_stack(1)
        else:
            QMessageBox.information(self.window, '!', '注册成功', QMessageBox.Yes)
            save_user_info(new_username, new_password)
            self.goto_stack(0)

    def goto_stack(self, index: int):
        """切换 StackWidget 页面"""
        self.username_input.clear()
        self.password_input.clear()
        self.new_username_input.clear()
        self.new_password_input.clear()
        self.confirm_password_input.clear()
        self.stacked_widget.setCurrentIndex(index)

    # 窗口拖动逻辑
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.window.isMaximized():
            self.mm_flag = True
            self.m_Position = event.globalPos() - self.window.pos()
            event.accept()
            self.window.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.mm_flag:
            self.window.move(event.globalPos() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.mm_flag = False
        self.window.setCursor(QCursor(Qt.ArrowCursor))