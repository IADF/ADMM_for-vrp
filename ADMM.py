############################head_file###################################
import copy
import include
import read_data
import gurobipy as gp

#############################program##################################
###########################################
#   动态规划(label_setting_algorithm)
#
#   by noir
###########################################
def dynamic_programming(agent_id,ADMM_num):
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
                    # include.sever_time[ADMM_num][]
                    dynamic_programming_list[include.link[i][j].spend_time].append(include.CVSState())
                    dynamic_programming_list[include.link[i][j].spend_time][z].node_id_record.append(i)  # 添加初始节点
                    dynamic_programming_list[include.link[i][j].spend_time][z].node_id_record.append(j)
                    dynamic_programming_list[include.link[i][j].spend_time][z].from_node_id = i
                    dynamic_programming_list[include.link[i][j].spend_time][z].to_node_id = j
                    dynamic_programming_list[include.link[i][j].spend_time][z].cost_time += include.link[0][j].spend_time
                    #   fix_cost
                    dynamic_programming_list[include.link[i][j].spend_time][z].label_cost += include.fixed_cost
                    #   distance_cost
                    dynamic_programming_list[include.link[i][j].spend_time][z].label_cost += include.link[0][j].distance/1000*12
                    #   penalty_cost


        #   列表为空时直接跳过
        elif len(dynamic_programming_list[i]) == 0:
            continue

        #   列表元素小于100时，直接进行动态规划
        elif len(dynamic_programming_list[i]) <= 100:  # 不足一百组
            for j in range(include.customer_size + 1):
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
                    continue

                for k in range(len(dynamic_programming_list[i])):
                    if 0 < include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time < include.transport_time_limit and \
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.arrival_time_ending and \
                        dynamic_programming_list[i][k].node_id_record.count(j) == 0 and\
                        include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + dynamic_programming_list[i][k].cost_time <= include.node[j].last_receive_time and\
                        include.node[j].pack_total_weight + include.agent[agent_id].agent_weight <= include.agent_weight_limit and\
                        include.node[j].pack_total_volume + include.agent[agent_id].agent_volume <= include.agent_volume_limit:

                        z = len(dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i])
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i].append(include.CVSState())
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z] = dynamic_programming_list[i][k]
                        #   record
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].node_id_record.append(j)
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].from_node_id = dynamic_programming_list[i][k].to_node_id
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].to_node_id = j
                        #   time
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].cost_time += \
                            include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time
                        #   distance_cost
                        dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].label_cost += \
                            (include.link[dynamic_programming_list[i][k].to_node_id][j].distance/1000 * 12)
                        #   waiting_cost
                        if include.wait_flag == include.wait:
                            dynamic_programming_list[include.link[dynamic_programming_list[i][k].to_node_id][j].spend_time + i][z].label_cost += \
                                0


        #   列表元素大于100时,进行排序对较好的前k组数据进行动态规划
        else:  #
            dynamic_programming_list[i].sort(key=lambda x:x.label_cost)
            for j in range(include.customer_size + 1):
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
                        continue



    for i in range(include.customer_size):
        include.sever_time[ADMM_num][i] = dynamic_programming_list[0].node_id_record.count(i)
    return 0

############################
#   ADMM算法迭代
#       output:输出动态规划中最好的结果
############################
def ADMM():
    for ADMM_iteration_num in range(include.ADMM_iteration):  # 迭代次数
        node_penalty = []  # 每个节点的惩罚函数
        # 创建一个数组存储每次迭代后的结果
        include.ADMM_iteration_cost_record.append([])
        for v in range(include.vehicle_fleet_size):
            include.ADMM_iteration_cost_record[i].append(include.CVSState)

        if ADMM_iteration_num != len(include.sever_time):    #
            z = len(include.sever_time)
            include.sever_time.append([])
            include.sever_time[z] = include.sever_time[z-1]
            for i in range(1,include.customer_size):   # 每次迭代时将服务过的节点访问次数-1
                include.sever_time[z][i] -=

        for v in range(include.vehicle_fleet_size):  # 利用动态规划对每个子问题进行求解
            # 计算罚函数（每个客户节点单独计算）
            for i in range(include.customer_size):
                node_penalty[i] = include.sever_time[ADMM_iteration_num][i]

            # 动态规划
            include.ADMM_iteration_cost_record[ADMM_iteration_num][v] = dynamic_programming(v,ADMM_iteration_num)
            print("agent" + str(v))

            for i in range(include.customer_size):    # 统计每个节点给访问的次数
                include.sever_time[ADMM_iteration_num][i] = include.ADMM_iteration_cost_record[ADMM_iteration_num][v].node_id_record.count(i)

        # 加一个很大的惩罚把一个非可行解的时间强行拉上去

    return 0 # Best_cost
