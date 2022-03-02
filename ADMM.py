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
    for i in range(include.service_time_begin, include.arrival_time_ending + 1):  #
        dynamic_programming_list.append([])

    for i in range(include.service_time_begin, include.arrival_time_ending + 1):
        #   first
        if i == 0:
            for j in range(include.customer_size):
                if 0 < include.link[i][j].spend_time <= include.transport_time_limit:
                    z = len(dynamic_programming_list[include.link[i][j].spend_time])
                    dynamic_programming_list[include.link[i][j].spend_time].append(include.CVSState())
                    dynamic_programming_list[include.link[i][j].spend_time][z].node_id_record.append(i)  # 添加初始节点
                    dynamic_programming_list[include.link[i][j].spend_time][z].node_id_record.append(j)
                    dynamic_programming_list[include.link[i][j].spend_time][z].from_node_id = i
                    dynamic_programming_list[include.link[i][j].spend_time][z].to_node_id = j
                    dynamic_programming_list[include.link[i][j].spend_time][z].cost_time += include.link[0][j].spend_time
                    #   成本代价计算
                    dynamic_programming_list[include.link[i][j].spend_time][z].label_cost += (include.link[i][j].distance/1000*12) + include.fixed_cost

        #   列表为空时直接跳过
        elif len(dynamic_programming_list[i]) == 0:
            continue

        #   列表元素小于100时，直接进行动态规划
        elif len(dynamic_programming_list[i]) <= 100:  # 不足一百组
            for j in range(include.customer_size + 1):
                if j == 100:    # 车辆到达了终止仓库
                    z = len(dynamic_programming_list[0])
                    dynamic_programming_list[0].append(include.CVSState())
                    dynamic_programming_list[0].[z]
                    continue

                for k in range(len(dynamic_programming_list[i])):
                    if 0 < include.link[dynamic_programming_list[i][k].to_node_id][
                        j].spend_time < include.transport_time_limit and \
                            include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + \
                            dynamic_programming_list[i][k].cost_time <= include.arrival_time_ending and \
                            dynamic_programming_list[i][k].node_id_record.count(
                                j) == 0:  # 单次运输时间过长and运输时间超过最大返回时间and访问已访问过的节点
                        z = len(dynamic_programming_list[
                                    include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i])

                        dynamic_programming_list[
                            include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i].append(
                            include.CVSState())
                        dynamic_programming_list[
                            include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z] = \
                        dynamic_programming_list[i][k]

        #   列表元素大于100时,进行排序对较好的前k组数据进行动态规划
        else:  #
            dynamic_programming_list[i].sort(key=lambda x:x.label_cost)
    return 0


#############################
#   calculate_cost(current_time,)
#       input:current_time(当前时间),对象，ADMM罚函数flag
#       output:label_cost or label_cost_lr
#############################
# def calculate_cost(current_time,pre_label_cost,wait_flag,ADMM_flag):
#     if current_time == 0:   # 初始化固定成本
#         cost = pre_label_cost +
#     return cost


############################
#
#   output:输出动态规划中最好的结果
############################
def ADMM():
    for i in range(include.ADMM_iteration):  # 迭代次数
        print("ADMM_iteration = " + str(i))
        for v in range(include.vehicle_fleet_size):  # 利用动态规划对每个子问题进行求解
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
