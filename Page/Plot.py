from Page.MainWindow import MainWindow
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QTimer
import serial  # 第三方库 pyserial
import serial.tools.list_ports
import pyqtgraph as pg
import time

class Plot(MainWindow):
    def __init__(self, ui_file):
        super().__init__(ui_file)
        self.start_button.clicked.connect(self.start_port)
        self.close_button.clicked.connect(self.close_port)
        
        # 找到占位的QWidget
        self.plot_container = self.central_widget.findChild(QWidget, "plotWidget")
        
        # 创建布局
        layout = QVBoxLayout(self.plot_container)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        
        # 创建pyqtgraph绘图窗口并添加到布局
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        
        # 配置图表属性
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel('left', '数值')
        self.plot_widget.setLabel('bottom', '时间 (秒)')
        self.plot_widget.setTitle('实时数据监测')
        
        # 创建曲线对象
        self.curve = self.plot_widget.plot(pen=pg.mkPen('b', width=2))
        
        # 初始化数据存储
        self.x_data = []
        self.y_data = []
        self.start_time = 0
        self.IsOpen = False
        self.IsPause = False
        
        # 创建定时器用于更新图表
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.count = 0  # 用于找到肌电信号
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
                self.curve.setData(self.x_data, self.y_data)
                self.timer.start(100)  # 每100ms更新一次图表
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

    def toggle_pause(self):  # 暂停绘图
        if not self.IsOpen:
            print("端口未打开，无法暂停")
            return
        self.IsPause = not self.IsPause  # 切换暂停状态
        state = "暂停" if self.IsPause else "继续"
        print(f"串口读取已{state}")

    def clear_message(self):
        # 清空绘图区域
        self.x_data = []
        self.y_data = []
        self.curve.setData(self.x_data, self.y_data)
        print("清空绘图数据")

    def update_plot(self):

        if not self.IsOpen or self.IsPause:
            return
        try:
            if self.serial_port.in_waiting > 0:
                data_line = self.serial_port.readline().decode('utf-8').strip()
                if self.count == 1:
                    return
                self.count = (self.count + 1) % 2  # 每两次读取一次数据
                try:
                    value = float(data_line)
                    current_time = time.time() - self.start_time
                    # 添加新数据点
                    self.x_data.append(current_time)
                    self.y_data.append(value)
                    
                    # 限制数据点数量，防止过多数据影响性能
                    max_points = 100
                    if len(self.x_data) > max_points:
                        self.x_data = self.x_data[-max_points:]
                        self.y_data = self.y_data[-max_points:]
                    
                    # 更新图表
                    self.curve.setData(self.x_data, self.y_data)
                except ValueError:
                    print(f"无法将数据转换为浮点数: {data_line}")
        except Exception as e:
            print(f"读取数据出错: {str(e)}")