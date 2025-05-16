from PySide6.QtWidgets import QTextEdit, QPushButton, QLabel
import serial  # 第三方库 pyserial
from Page.MainWindow import MainWindow
from PySide6.QtCore import QTimer
import pandas as pd

import numpy as np
class Learn(MainWindow):
    def __init__(self, ui_file):
        super().__init__(ui_file)
        self.message = self.central_widget.findChild(QTextEdit, "message")
        self.predict_button = self.central_widget.findChild(QPushButton, "StartPredict")
        self.label = self.central_widget.findChild(QTextEdit, "label")
        self.StopPredict_button = self.central_widget.findChild(QPushButton, "StopPredict")
        self.start_button.clicked.connect(self.start_port)
        self.close_button.clicked.connect(self.close_port) # 暂停按钮图标
        self.predict_button.clicked.connect(self.on_predict_button_clicked) #预测
        self.StopPredict_button.clicked.connect(self.stop_predict) # 停止预测
        self.data = []
        self.emg_buffer = []
        self.sensor_buffer = []
        # 定时器，用于读取串口数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)
        # 添加预测定时器
        self.prediction_timer = QTimer()
        self.prediction_timer.timeout.connect(self.predict)
        self.is_predicting = False

        # 创建指示灯
        self.status_indicator = self.central_widget.findChild(QLabel, "status")
        self.status_indicator.setStyleSheet(
            "background-color: red; border-radius: 8px; margin: 2px;"
        )
        # 创建指示灯状态监测定时器
        self.indicator_timer = QTimer()
        self.indicator_timer.timeout.connect(self.update_status_indicator)
        self.indicator_timer.start(1000)  # 每秒检查一次状态

    def read_serial_data(self):
        # 读取串口数据
        if MainWindow.IsOpen:
            try:
                if MainWindow.serial_port.in_waiting > 0:  # 检查是否有数据可读
                    line = MainWindow.serial_port.readline().decode('utf-8').strip()
                    self.message.append(f"{line}")
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
                        self.sensor_buffer = [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, Angle_x, Angle_y, Angle_z]
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
                            self.emg_buffer = [emg1, emg2]
                            
                    # 检查是否同时有肌电信号和传感器数据
                    if self.emg_buffer and self.sensor_buffer:
                        # 合并数据
                        combined_data = self.emg_buffer + self.sensor_buffer
                        self.data.append(combined_data)
                        # 限制数据长度为1000，超出时删除最早的数据
                        if len(self.data) > 1000:
                            self.data.pop(0)
                        # 清空缓冲区
                        self.emg_buffer = []
                        self.sensor_buffer = []
                        
            except Exception as e:
                self.message.append(f"读取数据失败：{str(e)}")

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

    def on_predict_button_clicked(self):
        if not MainWindow.IsOpen:
            # 串口未打开，只预测一次csv
            self.predict(use_csv=True)
        else:
            # 串口已打开，进入连续预测模式
            self.start_continuous_prediction()

    
    def start_continuous_prediction(self):
        if not self.is_predicting:
            self.is_predicting = True
            self.update_status_indicator()
            self.message.append("开始连续预测模式...")
            self.predict_button.setEnabled(False)
            self.StopPredict_button.setEnabled(True)
            self.predict(use_csv=False)  # 用self.data
            self.prediction_timer.start(1000)
    
    def predict(self, use_csv=False):
        import torch
        import os
        from torch.nn.utils.rnn import pad_sequence

        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        data_path = os.path.join(data_dir, "data.csv")
        if use_csv:
            if not os.path.exists(data_path):
                self.message.append("未找到data.csv,无法预测")
                return
            try:
                df = pd.read_csv(data_path, encoding='utf-8')
            except Exception as e:
                self.message.append(f"读取CSV失败:{str(e)}")
                return
        else:
            if len(self.data) < 1000:
                self.message.append("数据不足，无法进行预测")
                if self.is_predicting:
                    self.stop_predict()
                return
            columns = ['EMG_Raw1', 'EMG_Raw2', 'AccelX', 'AccelY', 'AccelZ',
                    'GyroX', 'GyroY', 'GyroZ', 'AngleX', 'AngleY', 'AngleZ']
            df = pd.DataFrame(self.data, columns=columns)

        try:
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                    "model", "transformer.pt")
            pkl_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                    "model", "transformer_scalar.pkl")
            with open(pkl_path, 'rb') as f:
                import pickle
                scaler = pickle.load(f)
            
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            features = df.values
            features = scaler.transform(features)
            input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(device)

            # 创建模块映射，解决找不到 'transformer' 模块的问题
            import sys
            from model import transformer
            sys.modules['transformer'] = transformer  # 将 model.transformer 映射为 transformer
            
            # 正确导入模型
            from model.transformer import TransformerClassifier
            # 添加完整路径的类名到安全列表
            from torch.serialization import add_safe_globals
            add_safe_globals([TransformerClassifier])
            
            # 然后加载模型
            model = TransformerClassifier(
                input_dim=11,  # 特征数量
                hidden_dim=64,
                output_dim=4,  # 类别数
                num_heads=4,
                num_layers=2
            ).to(device)
            model.load_state_dict(torch.load(model_path, map_location=device))
            model.eval()
            with torch.no_grad():
                outputs = model(input_tensor)
                if outputs.dim() > 1 and outputs.shape[-1] > 1:
                    _, predicted_class = torch.max(outputs, dim=-1)
                    predicted_class = predicted_class.item()
                    action_mapping = {
                        0: "静止",
                        1: "握拳",
                        2: "弯举",
                        3: "摆臂"
                    }
                    action = action_mapping.get(predicted_class, f"未知动作 ({predicted_class})")
                    result = f"预测动作: {action}"
                else:
                    result = f"预测值: {outputs.item():.4f}"
            self.label.clear()
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
            self.StopPredict_button.setEnabled(False)  # 仍然保持停止按钮可用
            self.label.clear()

    def update_status_indicator(self):
        """定时检查预测状态并更新指示灯"""
        if self.is_predicting:
            # 预测中 - 绿色
            self.status_indicator.setStyleSheet(
                "background-color: green; border-radius: 8px; margin: 2px; border: 1px solid darkgreen;"
            )
        else:
            # 未预测 - 红色
            self.status_indicator.setStyleSheet(
                "background-color: red; border-radius: 8px; margin: 2px; border: 1px solid darkred;"
            )


