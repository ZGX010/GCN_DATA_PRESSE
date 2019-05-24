import numpy as np
import os
import time
import datetime
import progressbar
import pandas as pd
import glob
from time import perf_counter


def main():
    # data = np.array([])
    # data1 = "2019-01-24 00:01:00"
    # data2 = "2019-01-24 01:01:50"
    # datatime = (datetime.datetime.strptime(data2,"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(data1,"%Y-%m-%d %H:%M:%S")).total_seconds()
    # print(datatime)
    # datatime = datetime.datetime.strptime(data2,"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(data1,"%Y-%m-%d %H:%M:%S")
    # print(datatime)
    # re = np.float64(data[1][2]) + np.float64(data[2][2])
    # print('re:',re)

    # read_star = perf_counter()
    # print('reading the CSV data ')
    # # data = np.loadtxt('./record_2019-01-24.csv', delimiter=",", dtype=np.str)
    # data = pd.read_csv('./record_2019-01-24.csv')
    # read_time = perf_counter() - read_star
    # print('Read data finshed use', read_time, '/s', ' data_shape:', data.shape)
    # print(data.head(4))
    #
    # data.columns = ['time','lineID','stationID','deviceID','status','userID','payType']
    # time_cov_star = perf_counter()
    # data['new_time'] = data['time'].apply(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    # time_cov_use_time = perf_counter() -time_cov_star
    # print('Time data has been convert to datetime use :',time_cov_use_time,'/s')
    #
    # time_slot = pd.date_range('2019-01-24 00:00:00',periods=289,freq='300s')
    # print('finish the time slot data',time_slot)

    path = os.path.join(os.getcwd(),'data')
    print(path)
    all_filename = os.listdir(path)
    print(all_filename)
    sorted(all_filename)

    for i in range(len(all_filename)):
        new_path = os.path.join(path,all_filename[i])

    print(new_path)
    day = str(all_filename[1][7:17])
    print(day)

    time_slot = pd.date_range(day+' 00:00:00',periods =289,freq = '300s')
    print(time_slot)

    np.savetxt(day+'.csv',all_input_data,detimer=',')

    # time_slot = pd.date_range()
    #
    # all_input_data = np.array([])
    # start_find_aim_data = perf_counter()
    # for i in range(288):
    #     aim_data = cut_aim_data(time_slot[i],time_slot[i+1],data)
    #     print(aim_data.head(4))
    #     # all_stat_5min = count_stationID(aim_data)#count all station input in five min as 1*81 array
    #     # all_input_data = np.vstack((all_input_data,all_stat_5min))
    # end_find_aim_data = perf_counter() - start_find_aim_data
    # print('out all the data use :',end_find_aim_data)
    # print(all_input_data)

    # aim_data = aim_data[(data['status'] ==1)]
    # print(aim_data)


    # in_station_data = choose_input_station(data)
    # print(in_station_data)

    # temp_data = data[:,4] # status col
    # in_station_index = np.argwhere( temp_data == str(1))
    # temp_data = data[:,2] # station ID col
    # station_index = np.argwhere(temp_data == str(0) )

def cut_aim_data(aim_slot_after,aim_slot_before,data):
    find_aim_time_slot_star = perf_counter()
    aim_data = data[(data['new_time'] > pd.to_datetime(aim_slot_after)) & (data['new_time']<pd.to_datetime(aim_slot_before))]
    aim_time_slot_star_use_time = perf_counter() - find_aim_time_slot_star
    print('cut aim time data of ',aim_slot_after,' use :',aim_time_slot_star_use_time,'/s')
    return aim_data

# def count_stationID(aim_slot_data):
#     num_stationID = np.array([])
#     for ID in range(81):
#         ID_count= ##
#         num_stationID = np.contect((num_stationID,ID_count))
#     return num_stationID

# def find_all_aim_file():
#     return



# def cut_to_five_min(input_data,star_time):



if __name__ == '__main__':
    main()