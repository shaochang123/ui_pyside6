from PySide6.QtWidgets import QWidget, QMessageBox, QLineEdit,QGraphicsScene, QGraphicsPixmapItem,QGraphicsView
from PySide6.QtCore import Qt, Signal,QObject
from PySide6.QtGui import QCursor,QPixmap
import csv
from PySide6.QtUiTools import QUiLoader
import os
import time
import paramiko

class Login(QObject):
    login_success = Signal()  # 定义登录成功信号

    def __init__(self, ui_file,user_path):
        super().__init__()
        # 加载UI文件
        self.user_path = user_path
        loader = QUiLoader()
        self.window = loader.load(ui_file, None)
        if not self.window:
            print("UI file loading failed")
            return
        """初始化控件"""
        self.stacked_widget = self.window.findChild(QWidget, "stackedWidget")
        self.username_input = self.window.findChild(QLineEdit, "lineEdit_6")
        self.password_input = self.window.findChild(QLineEdit, "lineEdit_7")
        self.new_username_input = self.window.findChild(QLineEdit, "lineEdit_3")
        self.new_password_input = self.window.findChild(QLineEdit, "lineEdit_4")
        self.confirm_password_input = self.window.findChild(QLineEdit, "lineEdit_5")
        self.img_view = self.window.findChild(QGraphicsView, "image")
        # 设置密码输入框为隐藏模式
        self.password_input.setEchoMode(QLineEdit.Password)
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
    #保存用户信息
    def save_user_info(self, username, pwd):
        """
        保存用户信息到远程Ubuntu服务器，如果连接失败则保存到本地
        
        参数:
            username: 用户名
            pwd: 密码
        """
        # 指定远程服务器信息
        remote_ip = "xxx.xxx.xxx.xxx"  # 服务器IP
        remote_user = "xxx"  # SSH用户名
        remote_pass = "xxx"  # SSH密码
        remote_path = "xxx"  # Ubuntu上的文件路径
        
        header = ['name', 'key']
        values = [{'name': username, 'key': pwd}]
        
        try:
            # 尝试连接服务器并保存
            # 创建SSH客户端
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote_ip, username=remote_user, password=remote_pass, timeout=5)
            
            # 创建SFTP客户端
            sftp = ssh.open_sftp()
            
            # 检查文件是否存在
            file_exists = False
            try:
                sftp.stat(remote_path)
                file_exists = True
            except FileNotFoundError:
                pass
            
            if file_exists:
                # 读取现有内容
                with sftp.file(remote_path, 'r') as f:
                    content = f.read().decode('utf-8')
            else:
                # 创建新文件并添加表头
                content = ','.join(header) + '\n'
            
            # 添加新用户
            content += f"{username},{pwd}\n"
            
            # 写回文件
            with sftp.file(remote_path, 'w') as f:
                f.write(content.encode('utf-8'))
                
            sftp.close()
            ssh.close()
            
            print(f"Info has been saved to {remote_ip}:{remote_path}")
            return True
        except Exception as e:
            print(f"Remote server error: {e}")
            print("Attempting to save locally instead...")
            
            # 保存到本地文件
            try:
                # 检查本地文件是否存在
                file_exists = os.path.exists(self.user_path)
                
                if file_exists:
                    # 读取现有内容
                    with open(self.user_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                else:
                    # 创建新文件并添加表头
                    content = ','.join(header) + '\n'
                
                # 添加新用户
                content += f"{username},{pwd}\n"
                
                # 写回文件
                with open(self.user_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"Info has been saved locally to {self.user_path}")
                return True
            except Exception as local_e:
                print(f"Failed to save locally: {local_e}")
                return False

    #获取用户名和密码
    def get_user_info(self):
        """
        从远程Ubuntu服务器获取用户信息
        
        返回:
            包含用户名和密码的字典
        """
        USERS = {}
        # 指定远程服务器信息
        remote_ip = "xxx.xxx.xxx.xxx"  # 服务器IP
        remote_user = "xxx"  # SSH用户名
        remote_pass = "xxx"  # SSH密码
        remote_path = "xxx"  # Ubuntu上的文件路径
        
        # 添加重试机制
        max_attempts = 1
        for attempt in range(max_attempts):
            try:
                # 创建SSH客户端
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(remote_ip, username=remote_user, password=remote_pass)
                
                # 创建SFTP客户端
                sftp = ssh.open_sftp()
                
                try:
                    # 读取文件
                    with sftp.file(remote_path, 'r') as f:
                        content = f.read().decode('utf-8').splitlines()
                    
                    # 解析CSV格式
                    if len(content) > 0:
                        # 跳过表头
                        for line in content[1:]:
                            row = line.split(',')
                            if len(row) >= 2:
                                USERS[row[0]] = row[1]
                except FileNotFoundError:
                    print(f"Warning: User information file not found on {remote_ip}")
                
                sftp.close()
                ssh.close()
                return USERS
                
            except Exception as e:
                if attempt < max_attempts - 1:
                    print(f"Attempt {attempt+1}/{max_attempts} to connect to {remote_ip} failed: {e}")
                    time.sleep(0.1)  # 等待1秒再尝试
                else:
                    print(f"Unable to connect to remote server {remote_ip}: {e}")
                    # 如果远程访问失败，尝试使用本地备份文件

                    if os.path.exists(self.user_path):
                        print(f"Using local backup file: {self.user_path}")
                        with open(self.user_path, 'r', encoding='utf-8') as f:
                            reader = csv.reader(f)
                            for row in reader:
                                if len(row) >= 2:
                                    USERS[row[0]] = row[1]
                    return USERS
    
    def sign_in(self):
        """登录逻辑"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        # 获取已注册用户信息
        USERS = self.get_user_info()
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
        USERS = self.get_user_info()
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
            self.save_user_info(new_username, new_password)
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

    def show_img(self,img_path):
        if not os.path.exists(img_path):
            print(f"Image file does not exist: {img_path}")
            return
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print("Image loading failed, please check the image format or path")
            return

        # 创建场景并加载图片
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)
        self.img_view.setScene(scene)  # 将场景设置到 QGraphicsView
        # 在Login类中添加
    def closeEvent(self, event):
        """在窗口关闭时断开连接"""
        self.disconnect_network_drive()
        event.accept()