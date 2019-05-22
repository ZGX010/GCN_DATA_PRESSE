import pandas as pd
import time
import numpy as np
from datetime import datetime

def main():

    data = pd.read_csv('./test.csv',usecols=['time', 'stationID','status'])
    print(data.head(3))
    data['new_time'] = data['time'].apply(lambda x:datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    # cut_the_data
    new_data = data[(data['new_time'] >= pd.to_datetime('2019-01-01 02:00:00')) & (data['new_time'] <= pd.to_datetime('2019-01-01 02:05:00'))]
    print(new_data)
    # find the status is 1
    new_data =new_data[(new_data['status'] == 1)]
    print(new_data)
    # count the number of the stationID
    number_of_5 = list(new_data.stationID).count(5)
    print(number_of_5)

def gerent_time_slot(file_name):
    #record_2019-01-01.csv
    for i in range(1,289):# one day can been slot to 288
        temp_str = file_name + ' '
    return list_of_time_slot


if __name__ == '__main__':
    main()