############################head_file###################################
import copy
import include
import read_data
import gurobipy as gp

#############################program##################################
###########################################
#   动态规划(label_setting_algorithm)
#   by noir
###########################################
def dynamic_programming(agent_id):
    dynamic_programming_list = [] * include.arrival_time_ending

    #   创建数组进行动态规划
    for i in range(include.service_time_begin, include.arrival_time_ending + 1):   #
        dynamic_programming_list.append([])

    for i in range(include.service_time_begin, include.arrival_time_ending+1):
        #   first
        if i == 0:
            for j in range(include.customer_size):
                if 0 < include.link[i][j].spend_time < 50:
                    z = len(dynamic_programming_list[include.link[i][j].spend_time])
                    dynamic_programming_list[include.link[i][j].spend_time].append(include.CVSState())
                    dynamic_programming_list[include.link[i][j].spend_time][z].node_id_record.append(i)     # 添加初始节点
                    dynamic_programming_list[include.link[i][j].spend_time][z].node_id_record.append(j)
                    dynamic_programming_list[include.link[i][j].spend_time][z].cost_time += include.link[0][i].spend_time
        if len(dynamic_programming_list[i]) == 0:
            continue

    #
    

    return 0

#############################
#   input:
#############################
def calculate_cost():

    return 0

############################
#
#   output:输出动态规划中最好的结果
############################
def ADMM():
    for i in range(include.ADMM_iteration):   # 迭代次数
        print("ADMM_iteration = " + str(i))
        for v in range(include.vehicle_fleet_size):   # 利用动态规划对每个子问题进行求解
            dynamic_programming(v)
            print("agent" + str(v))
    return Best_cost

########################################
#   求解器
#
#######################################
# def gurobi_(agent_id):
#      = gp.GRB()
#
#     return 0


