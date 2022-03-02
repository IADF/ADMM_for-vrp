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
vehicle_service_time = 30  # 车辆在每个客户点的服务时长
service_time_begin = 0  # 车辆开始服务时间
arrival_time_ending = 960  # 车辆服务终止时间
customer_size = 100  # 客户数
begin_node_id = 0  # 起始仓库id
end_node_id = 100  # 终点仓库id
ADMM_iteration = 100  # ADMM迭代次数
ADMM_upperbound = 999999  # ADMM上界(初始值给一个极大值)
ADMM_lowerbound = -999999  # ADMM下界(初始值给一个极小值)
transport_time_limit = 50   # 单次最长运输时间限制
fixed_cost = 200  # 固定成本200(启用车辆则需要添加)

#   wait_flag(标记车辆是否由于时间窗进行等待标志位)
no_wait = 0
wait = 1

#####################value############################
node = []  # 存储节点信息
link = []  # 存储节点间的距离
agent = []  # 存储车辆状态
no_sever_node = []  # 记录没有访问过的节点


#####################object###########################
##############################
#   出发节点：begin_node 0
#   结束节点：end_node 100
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
#       距离成本：(距离/1000)*12
##############################
class Agent:
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


############################
#   动态规划中的使用的对象
###########################
class CVSState:
    def __init__(self):
        self.node_id_record = []  # 用来纪录路径的节点顺序
        self.cost_time = 0 # 记录消耗时间
        self.label_cost_record = []  # 记录动态规划过程中的代价
        self.label_cost_record_lr = []  # 记录动态规划加入罚函数的代价
        self.label_cost= 0
        self.label_cost_lr = 0
        self.from_node_id = 0

