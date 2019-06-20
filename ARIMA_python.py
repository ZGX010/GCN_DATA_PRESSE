import numpy as np
import pandas as pd
import pmdarima as pm
# import matplotlib.pylab as plt
from sklearn.metrics import mean_squared_error
import multiprocessing

def diff(a,b):
    a = np.array(a)
    b = np.array(b)
    print(a-b)

def gen_one_station_pre(one_station):
    list_pre_15 = list()
    list_pre_30 = list()
    list_pre_45 = list()

    train = one_station[:7200 - 288 * 3-9]  # 876 0122-2305/0125-2355 stationID=1
    test = one_station[7200 - 288 * 3-9:]
    # print(train)
    # print(test)
    auto_modl = pm.auto_arima(train, start_p=1, start_q=1, start_P=1, start_Q=1,
                              max_p=13, max_q=13, max_P=13, max_Q=13, seasonal=True,
                              stepwise=True, suppress_warnings=True, D=0, max_D=10,
                              error_action='ignore')
    time_slot = pd.date_range('2019-01-23 00:05:00', periods=863, freq='300s')
    # print('time_slot',time_slot)
    # print('',one_station[:])

    # print(test.shape[0]-3)
    for i in range(test.shape[0]-2):
        print("time step %d"%i)
        if i <= (test.shape[0]-9):
            preds, conf_int = auto_modl.predict(n_periods=9, return_conf_int=True)  # 3/6/9 15/30/45min
            preds = preds.astype(int)
            list_pre_15.append(preds[2])
            list_pre_30.append(preds[5])
            list_pre_45.append(preds[8])
            updata = test[i:i+1]
            auto_modl.update(updata)
        elif (test.shape[0]-9) < i and i <=(test.shape[0]-6):
            preds, conf_int = auto_modl.predict(n_periods=6, return_conf_int=True)  # 3/6/9 15/30/45min
            preds = preds.astype(int)
            list_pre_15.append(preds[2])
            list_pre_30.append(preds[5])
            updata = test[i:i+1]
            auto_modl.update(updata)
        else:
            preds, conf_int = auto_modl.predict(n_periods=3, return_conf_int=True)  # 3/6/9 15/30/45min
            preds = preds.astype(int)
            list_pre_15.append(preds[2])
            updata = test[i:i+1]
            auto_modl.update(updata)
    # print('station ID:%d done'%i)
    return list_pre_15[7:],list_pre_30[4:],list_pre_45[1:]

def func(msg):
    return ["one " ,msg], ["two",msg] , ["three",msg]

def main():
    NUM_CORE = int(multiprocessing.cpu_count())

    pre_15 = list()
    pre_30 = list()
    pre_45 = list()

    data = pd.read_csv('Subway_instation_data.csv')
    print(data.shape[1])  # 81
    print(data.shape[0])  # 7199=288*25

    # data.columns = data.shape[]
    time_slot = pd.date_range('2019-01-01 00:05:00', periods=data.shape[0], freq='300s')
    data.index = time_slot
    data.columns = np.arange(81)
    # print(data.head(15))

    result = list()
    pool = multiprocessing.Pool(processes=NUM_CORE)
    for i in range(81):
        one_station_data = data[i]
        print('station_ID: %d '%i)
        result.append(pool.apply_async(gen_one_station_pre, (one_station_data,)))
    pool.close()
    pool.join()
    #result 81 itm in ram
    for res in result:
        list_pre_one_station =res.get()
        pre_15.append(list_pre_one_station[0])
        pre_30.append(list_pre_one_station[1])
        pre_45.append(list_pre_one_station[2])

    arr_pre15 = np.transpose(np.array(pre_15).reshape((81, 863)))
    arr_pre30 = np.transpose(np.array(pre_30).reshape((81, 863)))
    arr_pre45 = np.transpose(np.array(pre_45).reshape((81, 863)))
    np.savetxt('ARIMA_pre_15.csv', arr_pre15, fmt='%d', delimiter=',')
    np.savetxt('ARIMA_pre_30.csv', arr_pre30, fmt='%d', delimiter=',')
    np.savetxt('ARIMA_pre_45.csv', arr_pre45, fmt='%d', delimiter=',')

    #---------------------------------*-----------------------------
    # for i in range(81):
    #     one_station_data = data[i]
    #     print('station_ID: %d '%i)
    #     list_pre_15, list_pre_30, list_pre_45 = gen_one_station_pre(one_station_data)
    #     pre_15.append(list_pre_15)
    #     pre_30.append(list_pre_30)
    #     pre_45.append(list_pre_45)

    # arr_pre15 = np.transpose(np.array(pre_15).reshape((81,863)))
    # arr_pre30 = np.transpose(np.array(pre_30).reshape((81,863)))
    # arr_pre45 = np.transpose(np.array(pre_45).reshape((81,863)))
    # np.savetxt('ARIMA_pre_15.csv', arr_pre15, fmt='%f', delimiter=',')
    # np.savetxt('ARIMA_pre_30.csv', arr_pre30, fmt='%f', delimiter=',')
    # np.savetxt('ARIMA_pre_45.csv', arr_pre45, fmt='%f', delimiter=',')

    # pool = multiprocessing.Pool(processes=NUM_CORE)
    # result = list()
    # test_1 = list()
    # test_2 = list()
    # test_3 = list()
    # for i in range(10):
    #     msg = "hello %d" % (i)
    #     result.append(pool.apply_async(func, (msg,)))
    # pool.close()
    # pool.join()
    # print(result)
    # for res in result:
    #     data=res.get()
    #     test_1.append(data[0])
    #     test_2.append(data[1])
    #     test_3.append(data[2])
    #     print(res.get())
    # arr_list1= np.array(test_1)
    # arr_list2= np.array(test_2)
    # arr_list3= np.array(test_3)
    # print("list_array_1",arr_list1)
    # print("list_array_2",arr_list2)
    # print("list_array_3",arr_list3)
    #
    # print("Sub-process(es) done.")

if __name__ == '__main__':
    main()