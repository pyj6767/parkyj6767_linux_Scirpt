#!/usr/bin/env python
#Script Name : data_to_csv | Made by Young-Jun Park, yjpark29@postech.ac.kr
#Discription
#: From extracted_data folder, data files convert to csv format(by pandas)
#Condition
#: There is extracted folder in current directory

import os
import numpy as np
import pandas as pd
#import matplotlib as plt

pwd=os.getcwd()
ps=pwd.split('/')
ps.reverse()

file_list=os.listdir(pwd+'/extracted_data')

for i in file_list:
    data=pd.read_csv(pwd+'/extracted_data/'+i, names=[i])
    df = pd.DataFrame(data)
    if 'pasted_data' in locals():
        pasted_data = pd.concat([pasted_data, df], axis=1)
    else:
        pasted_data=df

f_name='pandas_total_data_{}_{}.csv'.format(ps[1],ps[0])
f_name_trans='pandas_total_data_transpose_{}_{}.csv'.format(ps[1],ps[0])

pasted_data.to_csv(f_name, mode='w')

#transpose
pasted_data=pasted_data.transpose()
pasted_data.to_csv(f_name_trans, mode='w')
