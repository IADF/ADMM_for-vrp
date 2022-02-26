# head_file

import csv
import xlrd

#####################static###########################

#####################value############################

#####################object###########################

##############################
#   出发节点：0
#   结束节点：100
#   车辆服务节点耗时：30
#############################
class node():
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
class link():
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

