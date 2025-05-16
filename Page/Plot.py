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
        self.show_button = self.central_widget.findChild(QPushButton, "show_button")
        self.show_button.clicked.connect(self.show_csv)
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
        self.x_data = []
        self.y_data = []
        self.y_data2 = []
  
        # 创建定时器用于更新图表
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        
        # 初始化3D图形
        self.x = 0
        self.y = 0
        self.z = 0
        self.setup_3d_cube(self.x, self.y, self.z)
        
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

    def update_plot(self):
        if not MainWindow.IsOpen:
            return
        try:
            if MainWindow.serial_port.in_waiting > 0:
                data_line = MainWindow.serial_port.readline().decode('utf-8').strip()
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
        
    def show_csv(self):
        """显示data.csv中的数据到图表和立方体上"""
        # 检查端口是否关闭
        if self.IsOpen:
            print("请先关闭串口后再查看CSV数据")
            return
            
        # 检查data.csv文件是否存在
        import os
        import pandas as pd
        
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        data_path = os.path.join(data_dir, "data.csv")
        
        if not os.path.exists(data_path):
            print(f"找不到文件: {data_path}")
            return
        
        try:
            # 读取CSV文件
            df = pd.read_csv(data_path)
            
            # 检查必需的列
            required_columns = ['EMG_Raw1', 'EMG_Raw2', 'AngleX', 'AngleY', 'AngleZ']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"CSV文件缺少必要列: {', '.join(missing_columns)}")
                return
                
            # 准备数据
            x_data = list(range(len(df)))
            emg1_data = df['EMG_Raw1'].tolist()
            emg2_data = df['EMG_Raw2'].tolist()
            
            # 更新图表
            self.curve.setData(x_data, emg1_data)
            self.curve2.setData(x_data, emg2_data)
            
            # 更新图表标题
            self.plot_widget.setTitle('EMG1数据 (从CSV文件)')
            self.plot_widget2.setTitle('EMG2数据 (从CSV文件)')
            
            # 自动调整坐标范围
            self.plot_widget.enableAutoRange()
            self.plot_widget2.enableAutoRange()
            
            # 存储所有角度数据用于动画
            self.angle_data = list(zip(df['AngleX'], df['AngleY'], df['AngleZ']))
            self.current_frame = 0

            # 创建动画定时器
            if hasattr(self, 'angle_timer'):
                self.angle_timer.stop()
                
            self.angle_timer = QTimer()
            self.angle_timer.timeout.connect(self.animate_angles)
            self.angle_timer.start(200)  # 20 FPS
            
            print(f"已加载 {len(df)} 条CSV数据记录")
            
        except Exception as e:
            import traceback
            print(f"读取CSV数据失败: {str(e)}")
            print(traceback.format_exc())

    def animate_angles(self):
        """动画展示立方体旋转"""
        if not hasattr(self, 'angle_data') or not self.angle_data:
            return
            
        # 更新当前帧
        self.current_frame = (self.current_frame + 1) % len(self.angle_data)
        
        # 获取当前帧的角度数据
        angle_x, angle_y, angle_z = self.angle_data[self.current_frame]
        
        # 更新立方体旋转
        self.update_cube_rotation(angle_x, angle_y, angle_z)
