###################################
#   include.py用途：
#   存放：
#       头文件
#       静态变量声明
#       全局变量声明
#       对象
#   by noir
##################################

####################head_file#########################
import csv
import xlrd
import numpy as np
import time
import read_data

#####################static###########################
vehicle_fleet_size = 16  # 车辆数
vehicle_service_time = 30   # 车辆在每个客户点的服务时长
arrival_time_ending = 960   # 车辆服务终止时间
customer_size = 100     # 客户数

#####################value############################
node = []   # 存储节点信息
link = []   # 存储节点间的距离
agent = []  # 存储车辆状态

#####################object###########################
##############################
#   出发节点：0
#   结束节点：100
#   车辆服务节点耗时：30
#############################
class Node():
    def __init__(self):
        self.node_id = 0
        self.type = 0
        self.longitude = 0  # 经度(lng)
        self.latitude = 0  # 纬度(lat)
        self.pack_total_weight = 0  # 货物重量
        self.pack_total_volume = 0  # 货物体积
        self.first_receive_time = 0  # 时间窗（begin）
        self.last_receive_time = 0  # 时间窗（end）


################################
#   记录不同节点间的距离和行驶时长
###############################
class Link():
    def __init__(self):
        self.link_id = 0
        self.from_node = 0
        self.to_node = 0
        self.distance = 0
        self.spend_time = 0


###############################
#   车辆参数：
#       限重：2.0
#       限体积：12.0
#       车辆数：16
#       车辆启动的固定成本：200
#       等待成本：0.4*time
#       发车时间：0
#       车辆返回时限：960
##############################
class Agent():
    def __init__(self):
        self.agent_id = 0
        self.from_node_id = 0
        self.to_node_id = 0
        self.agent_volume = 0
        self.agent_weight = 0
        self.running_time = 0  # 运行时间
        self.running_distance = 0  # 运行距离
        self.departure_time = 0  # 车辆离开节点时间
        self.arrival = 0  # 车辆到达节点时间
