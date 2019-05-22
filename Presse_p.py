import pandas as pd
import numpy as np

data = np.loadtxt('/home/zgx010/Desktop/p.csv',str,delimiter=',')
# print(data)
print(data.shape)
print(data.dtype)

link = np.array(['source','target','value'])
node = np.array(['name','group','size'])

for r in range(data.shape[0]): #reda data row
    node_id = r
    node_row = np.array([node_id,int(1),int(1)])
    node = np.vstack((node,node_row))
    data_lines = data[r]
    for c in range(r,data.shape[1]): #reda data col
        if data_lines[c] != str(0):
            # print(data_lines[c])
            link_cum = np.array([r,c,data_lines[c]]) # [sorce, tagert,value]
            # print(link_cum)
            # np.vstack((link,link_cum))
            link = np.vstack((link,link_cum))
            # link.append(link_cum)
print(link)
np.savetxt('/home/zgx010/Desktop/link.csv',link,fmt='%s',delimiter=',')
np.savetxt('/home/zgx010/Desktop/node.csv',node,fmt='%s',delimiter=',')
print('the link csv have been saved')