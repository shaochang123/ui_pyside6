from PySide6.QtWidgets import QTextEdit, QPushButton
import serial  # 第三方库 pyserial
from Page.MainWindow import MainWindow
from PySide6.QtCore import QTimer
import pandas as pd
class Learn(MainWindow):
    def __init__(self, ui_file):
        super().__init__(ui_file)
        self.message = self.central_widget.findChild(QTextEdit, "message")
        self.predict_button = self.central_widget.findChild(QPushButton, "StartPredict")
        self.label = self.central_widget.findChild(QTextEdit, "label")
        self.StopPredict_button = self.central_widget.findChild(QPushButton, "StopPredict")
        self.start_button.clicked.connect(self.start_port)
        self.close_button.clicked.connect(self.close_port) # 暂停按钮图标
        self.predict_button.clicked.connect(self.predict) #预测
        self.StopPredict_button.clicked.connect(self.stop_predict) # 停止预测
        self.data = []
        # 定时器，用于读取串口数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)
        # 添加预测定时器
        self.prediction_timer = QTimer()
        self.prediction_timer.timeout.connect(self.predict)
        self.is_predicting = False
    def read_serial_data(self):
        # 读取串口数据
        if self.IsOpen and not self.IsPause:
            try:
                if self.serial_port.in_waiting > 0:  # 检查是否有数据可读
                    line = self.serial_port.readline().decode('utf-8').strip()
                    if "A" in line:
                        # 将键值对格式的字符串转换为字典
                        values_dict = {}
                        pairs = line.split(',')
                        for pair in pairs:
                            if ':' in pair:  # 确保有冒号再进行分割
                                key, value = pair.split(':')
                                if value == '-' or value == '':
                                    continue
                                values_dict[key.strip()] = float(value.strip())
                            else:
                                continue
                        # 提取需要的值
                        accel_x = values_dict.get('AccelX')
                        accel_y = values_dict.get('AccelY')
                        accel_z = values_dict.get('AccelZ')
                        gyro_x = values_dict.get('GyroX')
                        gyro_y = values_dict.get('GyroY')
                        gyro_z = values_dict.get('GyroZ')
                        Angle_x = values_dict.get('AngleX')
                        Angle_y = values_dict.get('AngleY')
                        Angle_z = values_dict.get('AngleZ')
                        # 将加速度和陀螺仪数据存储到缓冲区
                        sensor_buffer = [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, Angle_x, Angle_y, Angle_z]
                    # 处理第二种格式（数值列表，表示肌电信号和检测值）
                    else:
                        values_dict = {}# 修改数据处理部分代码
                        values_dict = {}
                        pairs = line.split(',')
                        for pair in pairs:
                            if ':' in pair:  # 确保有冒号再进行分割
                                key, value = pair.split(':')
                                if value == '-' or value == '':
                                    continue
                                values_dict[key.strip()] = float(value.strip())
                            else:
                                continue  # 跳过格式不正确的数据

                        # 检查必要的键是否存在
                        if 'EMG1' in values_dict and 'EMG2' in values_dict:
                            emg1 = values_dict.get('EMG1')
                            emg2 = values_dict.get('EMG2')
                            emg_buffer = [emg1, emg2]
                    # 检查是否同时有肌电信号和传感器数据
                    if emg_buffer and sensor_buffer:
                        # 合并数据
                        combined_data = emg_buffer + sensor_buffer
                        self.data.append(combined_data)
                        # 限制数据长度为1000，超出时删除最早的数据
                        if len(self.data) > 1000:
                            self.data.pop(0)
                        # 清空缓冲区
                        emg_buffer = []
                        sensor_buffer = []
                        
            except Exception as e:
                self.message.append(f"读取数据失败：{str(e)}")
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
    def start_continuous_prediction(self):
        if not self.is_predicting:
            self.is_predicting = True
            self.message.append("开始连续预测模式...")
            self.predict_button.setEnabled(False)  # 禁用开始按钮
            self.StopPredict_button.setEnabled(True)  # 启用停止按钮
            # 立即进行一次预测
            self.predict()
            # 启动定时器，每1秒进行一次预测
            self.prediction_timer.start(1000)  # 每秒预测一次，可以根据需要调整时间

    def predict(self):
        import torch
        import os
        import numpy as np
        from torch.nn.utils.rnn import pad_sequence

        if len(self.data) < 1000:
            self.message.append("数据不足，无法进行预测")
            if self.is_predicting:
                self.stop_predict()
            return

        try:
            # 将收集的数据转换为DataFrame
            columns = ['EMG_Raw1', 'EMG_Raw2', 'AccelX', 'AccelY', 'AccelZ', 
                      'GyroX', 'GyroY', 'GyroZ', 'AngleX', 'AngleY', 'AngleZ']
            df = pd.DataFrame(self.data, columns=columns)
            
            # 如果是连续预测模式，就不需要每次都显示预处理信息
            if not self.is_predicting:
                self.message.append("开始数据预处理...")
            
            features = df.values  # 获取数值数据
            
            # 转换为PyTorch张量
            input_tensor = torch.FloatTensor(features)
            
            # 根据模型要求调整形状 - 添加批次维度
            if len(input_tensor.shape) == 2:  # [seq_len, features]
                input_tensor = input_tensor.unsqueeze(0)  # [1, seq_len, features]
            
            # 加载模型
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     "model", "transformer.pt")
            
            # 如果是连续预测模式，就不需要每次都显示加载信息
            if not self.is_predicting:
                self.message.append(f"加载模型：{model_path}...")
            
            # 检查CUDA是否可用
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            
            # 如果是连续预测模式，就不需要每次都显示设备信息
            if not self.is_predicting:
                self.message.append(f"使用设备: {device}")
            
            # 加载模型
            model = torch.load(model_path, map_location=device)
            model.eval()  # 设置为评估模式
            
            # 将数据移动到相同的设备
            input_tensor = input_tensor.to(device)
            
            # 进行预测
            with torch.no_grad():
                outputs = model(input_tensor)
                
                # 根据模型输出类型处理结果
                # 假设是分类任务
                if outputs.dim() > 1 and outputs.shape[-1] > 1:
                    # 获取预测的类别
                    _, predicted_class = torch.max(outputs, dim=-1)
                    predicted_class = predicted_class.item()
                    
                    # 映射类别到具体动作（根据您的实际情况调整）
                    action_mapping = {
                        0: "静止",
                        1: "握拳",
                        2: "伸展",
                        3: "抓取",
                        4: "放松"
                        # 根据需要添加更多映射
                    }
                    
                    action = action_mapping.get(predicted_class, f"未知动作 ({predicted_class})")
                    result = f"预测动作: {action}"
                else:
                    # 如果是回归任务
                    result = f"预测值: {outputs.item():.4f}"
            
            # 显示预测结果
            self.label.setText(result)
            
        except FileNotFoundError:
            self.message.append("错误：找不到模型文件！请检查模型路径。")
            if self.is_predicting:
                self.stop_predict()
        except Exception as e:
            self.message.append(f"预测过程中出错: {str(e)}")
            import traceback
            self.message.append(traceback.format_exc())
            if self.is_predicting:
                self.stop_predict()

    def stop_predict(self):
        if self.is_predicting:
            self.prediction_timer.stop()
            self.is_predicting = False
            self.message.append("已停止连续预测")
            self.predict_button.setEnabled(True)  # 重新启用开始按钮
            self.StopPredict_button.setEnabled(True)  # 仍然保持停止按钮可用


