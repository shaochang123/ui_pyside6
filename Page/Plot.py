from Page.MainWindow import MainWindow
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QTimer
import serial  # 第三方库 pyserial
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import time
class Plot(MainWindow):
    def __init__(self, ui_file):
        super().__init__(ui_file)
        self.reset_button = self.central_widget.findChild(QPushButton, "reset_button")
        self.start_button.clicked.connect(self.start_port)
        self.close_button.clicked.connect(self.close_port)
        self.reset_button.clicked.connect(self.reset)
        # 找到占位的QWidget
        self.plot_container = self.central_widget.findChild(QWidget, "plotWidget")
        # 找到占位的QWidget
        self.plot_container2 = self.central_widget.findChild(QWidget, "plotWidget2")

        # 创建布局
        layout = QVBoxLayout(self.plot_container)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        layout2 = QVBoxLayout(self.plot_container2)
        layout2.setContentsMargins(0, 0, 0, 0)  # 移除边距
        # 创建pyqtgraph绘图窗口并添加到布局
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        self.plot_widget2 = pg.PlotWidget()
        layout2.addWidget(self.plot_widget2)
        # 配置图表属性
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel('left', '通道一数值')
        self.plot_widget.setLabel('bottom', '时间 (秒)')
        self.plot_widget.setTitle('实时数据监测')
        self.plot_widget2.setBackground('w')
        self.plot_widget2.showGrid(x=True, y=True)
        self.plot_widget2.setLabel('left', '通道二数值')
        self.plot_widget2.setLabel('bottom', '时间 (秒)')
        self.plot_widget2.setTitle('实时数据监测')
        # 创建曲线对象
        self.curve = self.plot_widget.plot(pen=pg.mkPen('b', width=2))
        self.curve2 = self.plot_widget2.plot(pen=pg.mkPen('b',width=2))
        self.start_time = 0
        self.IsOpen = False
        self.IsPause = False
        
        # 创建定时器用于更新图表
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        
        # 初始化3D图形
        self.x = 0
        self.y = 0
        self.z = 0
        self.setup_3d_cube(self.x, self.y, self.z)
        
    def start_port(self):
        if self.IsOpen:
            print("端口已经打开")
            return
        # 获取端口号和波特率
        port = self.com_name.toPlainText().strip()
        baud_rate = self.bote_name.toPlainText().strip()

        if not port or not baud_rate:
            print("启动端口失败：端口号或波特率为空")
            return

        # 打开端口逻辑
        try:
            self.serial_port = serial.Serial(port, int(baud_rate), timeout=1)
            self.IsOpen = self.serial_port.is_open
            if self.IsOpen:
                # 画图初始化
                self.start_time = time.time()  # 记录开始时间
                self.x_data = []
                self.y_data = []
                self.y_data2 = []
                self.curve.setData(self.x_data, self.y_data)
                self.curve2.setData(self.x_data,self.y_data2)
                self.timer.start(50)  # 每50ms更新一次图表
                print("端口打开成功，开始绘制数据...")
            else:
                print("启动端口失败")
        except Exception as e:
            print(f"启动端口失败：{str(e)}")

    def close_port(self):  # 关闭端口
        if not self.IsOpen:
            print("端口未打开")
            return
        # 关闭端口逻辑
        try:
            if self.serial_port:
                self.serial_port.close()
            self.IsOpen = False
            self.timer.stop()  # 停止定时器
            print("关闭端口成功")
        except Exception as e:
            print(f"关闭端口失败：{str(e)}")

    def update_plot(self):
        if not self.IsOpen or self.IsPause:
            return
        try:
            if self.serial_port.in_waiting > 0:
                data_line = self.serial_port.readline().decode('utf-8').strip()
                if data_line[0] == 'A':
                    data_line = data_line.split(',')
                    x = float(data_line[6].split(':')[1])
                    y = float(data_line[7].split(':')[1])
                    z = float(data_line[8].split(':')[1])
                    self.update_cube_rotation(x, y, z)
                    return
                data_line = data_line.split(',')  # 取第一个数据点
                try:
                    value1 = float(data_line[0].split(':')[1])
                    value2 = float(data_line[2].split(':')[1])
                    current_time = time.time() - self.start_time
                    # 添加新数据点
                    self.x_data.append(current_time)
                    self.y_data.append(value1)
                    self.y_data2.append(value2)
                    # 限制数据点数量，防止过多数据影响性能
                    max_points = 100
                    if len(self.x_data) > max_points:
                        self.x_data = self.x_data[-max_points:]
                        self.y_data = self.y_data[-max_points:]
                        self.y_data2 = self.y_data2[-max_points:]
                    
                    # 更新图表
                    self.curve.setData(self.x_data, self.y_data)
                    self.curve2.setData(self.x_data, self.y_data2)
                except ValueError:
                    print(f"无法将数据转换为浮点数: {data_line}")
        except Exception as e:
            print(f"读取数据出错: {str(e)}")
            
    def setup_3d_cube(self, grok_x=0, grok_y=0, grok_z=0):
        """
        设置3D正方体并根据传入的角度调整姿态
        
        参数:
            grok_x (float): X轴旋转角度(度)
            grok_y (float): Y轴旋转角度(度)
            grok_z (float): Z轴旋转角度(度)
        """
        # 找到3D容器
        self.cube_container = self.central_widget.findChild(QWidget, "cube3dContainer")
        
        # 创建布局
        layout = QVBoxLayout(self.cube_container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建OpenGL视图
        self.view_3d = gl.GLViewWidget()
        layout.addWidget(self.view_3d)
        
        # 创建3D网格
        self.grid = gl.GLGridItem()
        self.view_3d.addItem(self.grid)
        
        # 创建立方体顶点
        vertices = np.array([
            [2, 2, 2], [2, 2, -2], [2, -2, 2], [2, -2, -2],
            [-2, 2, 2], [-2, 2, -2], [-2, -2, 2], [-2, -2, -2]
        ])
        
        # 定义立方体的面
        faces = np.array([
            [0, 1, 2], [1, 3, 2],  # 右面
            [4, 5, 6], [5, 7, 6],  # 左面
            [0, 1, 4], [1, 5, 4],  # 前面
            [2, 3, 6], [3, 7, 6],  # 后面
            [0, 2, 4], [2, 6, 4],  # 上面
            [1, 3, 5], [3, 7, 5],  # 下面
        ])
        
        # 创建并设置立方体的颜色
        colors = np.array([
            [1, 0, 0, 1], [1, 0, 0, 1],  # 右面 (红色)
            [0, 1, 0, 1], [0, 1, 0, 1],  # 左面 (绿色)
            [0, 0, 1, 1], [0, 0, 1, 1],  # 前面 (蓝色)
            [1, 1, 0, 1], [1, 1, 0, 1],  # 后面 (黄色)
            [1, 0, 1, 1], [1, 0, 1, 1],  # 上面 (紫色)
            [0, 1, 1, 1], [0, 1, 1, 1],  # 下面 (青色)
        ])
        
        # 创建立方体网格对象
        self.cube = gl.GLMeshItem(vertexes=vertices, faces=faces, faceColors=colors, smooth=False)
        self.view_3d.addItem(self.cube)
        
        # 设置相机位置
        self.view_3d.setCameraPosition(distance=10)
        
        # 应用旋转
        self.update_cube_rotation(grok_x, grok_y, grok_z)

    def update_cube_rotation(self, x_angle, y_angle, z_angle):
        """
        更新立方体旋转角度
        
        参数:
            x_angle (float): X轴旋转角度(度)
            y_angle (float): Y轴旋转角度(度)
            z_angle (float): Z轴旋转角度(度)
        """
        if hasattr(self, 'cube'):
            # 重置立方体方向
            self.cube.resetTransform()
            
            # 按顺序应用旋转（先X，再Y，最后Z）
            self.cube.rotate(x_angle, 1, 0, 0)
            self.cube.rotate(y_angle, 0, 1, 0)
            self.cube.rotate(z_angle, 0, 0, 1)
    def reset(self):
        self.x = 0
        self.y = 0
        self.z = 0
    