import time
import include
import read_data
import ADMM

########################################
#
if __name__ == '__main__':
    #   读取表格数据
    read_data.read_data()

    #   ADMM
    start_time = time.time()

    ADMM.ADMM()

    end_time = time.time()
    print("total_running_time" + str(start_time-end_time))
