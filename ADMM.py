############################head_file###################################
import copy
import time

import include
import read_data
import gurobipy as gp

#############################program##################################
###########################################
#   动态规划(label_setting_algorithm)
#
#   by noir
###########################################
def dynamic_programming(agent_id):
    dynamic_programming_list = [] * include.arrival_time_ending

    #   创建数组进行动态规划
    for i in range(include.service_time_begin, include.arrival_time_ending + 1):  #
        dynamic_programming_list.append([])

    for i in range(include.service_time_begin, include.arrival_time_ending + 1):
        #   从起始点出发
        if i == 0:
            for j in range(include.customer_size):
                if 0 < include.link[i][j].spend_time <= include.transport_time_limit:

                    z = len(dynamic_programming_list[include.link[i][j].spend_time])
                    # include.sever_time[]
                    dynamic_programming_list[include.link[i][j].spend_time].append(include.CVSState())
                    dynamic_programming_list[include.link[i][j].spend_time][z].node_id_record.append(i)  # 添加初始节点
                    dynamic_programming_list[include.link[i][j].spend_time][z].node_id_record.append(j)
                    dynamic_programming_list[include.link[i][j].spend_time][z].from_node_id = i
                    dynamic_programming_list[include.link[i][j].spend_time][z].to_node_id = j
                    dynamic_programming_list[include.link[i][j].spend_time][z].cost_time += include.link[0][j].spend_time
                    dynamic_programming_list[include.link[i][j].spend_time][z].weight = include.node[j].pack_total_weight
                    dynamic_programming_list[include.link[i][j].spend_time][z].volume = include.node[j].pack_total_volume

                    #   fix_cost
                    dynamic_programming_list[include.link[i][j].spend_time][z].label_cost += include.fixed_cost
                    #   distance_cost
                    dynamic_programming_list[include.link[i][j].spend_time][z].label_cost += include.link[0][j].distance/1000*12
                    #   penalty_cost
                    for p in range(include.customer_size):
                        if p == j:
                            dynamic_programming_list[include.link[i][j].spend_time][z].label_cost += abs(1-(include.sever_time[j]+1)) * include.node_penalty[p]
                        else:
                            dynamic_programming_list[include.link[i][j].spend_time][z].label_cost += abs(1-include.sever_time[j]) * include.node_penalty[p]
                    #   wait_cost
                    wait_time = include.node[j].first_receive_time - dynamic_programming_list[include.link[i][j].spend_time][z].cost_time
                    if wait_time > 0:
                        dynamic_programming_list[include.link[i][j].spend_time][z].label_cost += 0.4 * (wait_time)   # 0.4单位等待成本
                        dynamic_programming_list[include.link[i][j].spend_time][z].cost_time = include.node[j].first_receive_time   # 等待

        #   列表为空时直接跳过
        elif len(dynamic_programming_list[i]) == 0:
            continue

        #   列表元素小于100时，直接进行动态规划
        elif len(dynamic_programming_list[i]) <= 100:  # 不足一百组
            for j in range(1,include.customer_size + 1):
                for k in range(len(dynamic_programming_list[i])):
                    # 车辆到达了终止仓库
                    if j == 100 and \
                        0 < include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time < include.transport_time_limit and \
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.arrival_time_ending and \
                        dynamic_programming_list[i][k].node_id_record.count(j) == 0 and \
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.node[j].last_receive_time and \
                        include.node[j].pack_total_weight + include.agent[agent_id].agent_weight <= include.agent_weight_limit and \
                        include.node[j].pack_total_volume + include.agent[agent_id].agent_volume <= include.agent_volume_limit:

                        # 单次运输时间过长and运输时间超过最大返回时间and访问未访问过的节点and时间小于最晚要求时间窗and载货小于车辆载货重量限制and载货体积小于车辆载货体积限制
                        z = len(dynamic_programming_list[0])
                        dynamic_programming_list[0].append(include.CVSState())
                        dynamic_programming_list[0][z] = copy.deepcopy(dynamic_programming_list[i][k])
                        #   record
                        dynamic_programming_list[0][z].node_id_record.append(j)
                        dynamic_programming_list[0][z].from_node_id = dynamic_programming_list[i][k].to_node_id
                        dynamic_programming_list[0][z].to_node_id = j
                        #   time
                        dynamic_programming_list[0][z].cost_time += include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time
                        #   distance_cost
                        dynamic_programming_list[0][z].label_cost += include.link[dynamic_programming_list[i][k].to_node_id][j].distance/1000*12
                        #   penalty_cost
                        for p in range(1,include.customer_size):
                            if dynamic_programming_list[0][z].node_id_record.count(p) != 0:
                                dynamic_programming_list[0][z].label_cost += \
                                    abs(1-(include.sever_time[p]+1)) * include.node_penalty[p]
                            else:
                                dynamic_programming_list[0][z].label_cost += \
                                    abs(1 - include.sever_time[p]) * include.node_penalty[p]
                        continue

                    if 0 < include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time < include.transport_time_limit and \
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.arrival_time_ending and \
                        dynamic_programming_list[i][k].node_id_record.count(j) == 0 and\
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.node[j].last_receive_time and\
                        include.node[j].pack_total_weight + dynamic_programming_list[i][k].weight <= include.agent_weight_limit and\
                        include.node[j].pack_total_volume + dynamic_programming_list[i][k].volume <= include.agent_volume_limit:

                        z = len(dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i])
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i].append(include.CVSState())
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z] = copy.deepcopy(dynamic_programming_list[i][k])
                        #   record
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].node_id_record.append(j)
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].from_node_id = dynamic_programming_list[i][k].to_node_id
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].to_node_id = j
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].weight += include.node[j].pack_total_weight
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].volume += include.node[j].pack_total_volume
                        #   time
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].cost_time += \
                            include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time
                        #   distance_cost
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].label_cost += \
                            (include.link[dynamic_programming_list[i][k].to_node_id][j].distance/1000 * 12)
                        #   waiting_cost
                        wait_time = include.node[j].first_receive_time - dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].cost_time
                        if wait_time > 0:
                            dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].label_cost += \
                                0.4 * wait_time
                            dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].cost_time = include.node[j].first_receive_time


        #   列表元素大于100时,进行排序对较好的前k组数据进行动态规划
        else:  #
            dynamic_programming_list[i].sort(key=lambda x:x.label_cost)
            for j in range(1,include.customer_size + 1):
                for k in range(100):    # 只取前100组较好的数据进行动态规划
                    # 车辆到达了终止仓库
                    if j == 100 and \
                        0 < include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time < include.transport_time_limit and \
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.arrival_time_ending and \
                        dynamic_programming_list[i][k].node_id_record.count(j) == 0 and\
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.node[j].last_receive_time and\
                        include.node[j].pack_total_weight + include.agent[agent_id].agent_weight <= include.agent_weight_limit and\
                        include.node[j].pack_total_volume + include.agent[agent_id].agent_volume <= include.agent_volume_limit:

                        z = len(dynamic_programming_list[0])
                        dynamic_programming_list[0].append(include.CVSState())
                        dynamic_programming_list[0][z] = copy.deepcopy(dynamic_programming_list[i][k])
                        #   record
                        dynamic_programming_list[0][z].node_id_record.append(j)
                        dynamic_programming_list[0][z].from_node_id = dynamic_programming_list[i][k].to_node_id
                        dynamic_programming_list[0][z].to_node_id = j
                        #   time
                        dynamic_programming_list[0][z].cost_time += include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time
                        #   distance_cost
                        dynamic_programming_list[0][z].label_cost += include.link[dynamic_programming_list[i][k].to_node_id][j].distance/1000*12
                        #   penalty_cost
                        for p in range(1,include.customer_size):
                            if dynamic_programming_list[0][z].node_id_record.count(p) != 0:
                                dynamic_programming_list[0][z].label_cost += \
                                    abs(1-(include.sever_time[p]+1)) * include.node_penalty[p]
                            else:
                                dynamic_programming_list[0][z].label_cost += \
                                    abs(1 - include.sever_time[p]) * include.node_penalty[p]
                        continue

                    if 0 < include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time < include.transport_time_limit and \
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.arrival_time_ending and \
                        dynamic_programming_list[i][k].node_id_record.count(j) == 0 and\
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.node[j].last_receive_time and\
                        include.node[j].pack_total_weight + dynamic_programming_list[i][k].weight <= include.agent_weight_limit and\
                        include.node[j].pack_total_volume + dynamic_programming_list[i][k].volume <= include.agent_volume_limit:

                        z = len(dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i])
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i].append(include.CVSState())
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z] = copy.deepcopy(dynamic_programming_list[i][k])
                        #   record
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].node_id_record.append(j)
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].from_node_id = dynamic_programming_list[i][k].to_node_id
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].to_node_id = j
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].weight += include.node[j].pack_total_weight
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].volume += include.node[j].pack_total_volume

                        #   time
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].cost_time += \
                            include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time
                        #   distance_cost
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].label_cost += \
                            (include.link[dynamic_programming_list[i][k].to_node_id][j].distance/1000 * 12)
                        #   waiting_cost
                        wait_time = include.node[j].first_receive_time - dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].cost_time
                        if wait_time > 0:
                            dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].label_cost += \
                                0.4 * wait_time
                            dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].cost_time = include.node[j].first_receive_time

    dynamic_programming_list[0].sort(key=lambda x: x.label_cost)
    for i in range(1,include.customer_size):
        include.sever_time[i] += dynamic_programming_list[0][0].node_id_record.count(i)
    print(dynamic_programming_list[0][0].node_id_record)
    print(dynamic_programming_list[0][0].cost_time)
    print(dynamic_programming_list[0][0].label_cost)
    return 0

############################
#



############################
#   ADMM算法迭代
#       output:输出动态规划中最好的结果
############################
def ADMM():
    #   初始化罚函数系数
    for i in range(include.customer_size):
        include.node_penalty.append(200)
        include.sever_time.append(0)

    for ADMM_iteration_num in range(include.ADMM_iteration):  # 迭代次数
        for i in range(include.customer_size):
            include.sever_time[i] = 0

        for v in range(include.vehicle_fleet_size):  # 利用动态规划对每个子问题进行求解

            # 动态规划include.ADMM_iteration_cost_record[ADMM_iteration_num][v] =
            dynamic_programming(v)
            print("agent" + str(v))

            # 计算罚函数系数（每个客户节点单独计算）
            for i in range(include.customer_size):
                include.node_penalty[i] += 20 * abs(1 - include.sever_time[i])    # 后面在调参

        for i in range(include.customer_size):
            print(include.sever_time[i])

    return 0 # Best_cost
