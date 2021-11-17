#!/usr/bin/env python
#Script Name : Choose_Selective_Dynamics.py
#Description
#: Choose_Selective_Dynamcis Selection for Slab

import sys
import numpy as np
import pandas as pd


if len(sys.argv) == 2:
    abc_select=int(sys.argv[1])
    bulk_layer_number=int(sys.argv[2])

elif len(sys.argv) > 2:
    print('Number of Argument must be 1!')
    print('Choose_Selective_Dynamics [abc_select(number)]')
    quit()

elif len(sys.argv) < 2:
    print('User Interactive Mode')
    
POSCARfile = open('POSCAR','r')

linedata=POSCARfile.readlines()

for i in range(len(linedata)):
    if linedata[i].find('Direct')>-1:
        dc=i
    elif linedata[i].find('Cartesian')>-1:
        dc=i

sd=False
for j in range(len(linedata)):
    if linedata[j].find('Selective')>-1:
        sd = True

if sd==True:
    sd=''
elif sd==False:
    sd='Selective Dynamics\n'
        
coordinates=linedata[dc+1:]

coordi=[]
for i in range(len(coordinates)):
    coordinates[i]=coordinates[i].replace('\n','').replace('\r','')
    coordi.append(coordinates[i].split(' '))

for j in range(len(coordi)):
    coordi[j] = [k for k in coordi[j] if k != '']

for p in range(len(coordi)):
    if len(coordi[p])>3: #TTT, FFF 까지 있는 데이터라면, 앞부분만 자르기
        coordi[p]=coordi[p][0:3]

for y in range(len(coordi)):
    coordi[y] = [float(u) for u in coordi[y]]

#000 check
for m in range(len(coordi)):
    if len(coordi[m])==0:
        checkpoint=m

if 'checkpoint' in globals():
    coordi=coordi[0:checkpoint]

abc_select=input('Select Slab Axis (a : 1, b : 2, c : 3) : ')

if abc_select=='1':
    abc_select='a'
elif abc_select=='2':
    abc_select='b'
else:
    abc_select='c'

axis_set=[]
for i in coordi:
    if abc_select=='a':
        axis_set.append(i[0])
    elif abc_select=='b':
        axis_set.append(i[1])
    elif abc_select=='c':
        axis_set.append(i[2])

axis_set=list(set(axis_set))
axis_set.sort(reverse=True)

print('Net {}-Axis Coordinates'.format(abc_select))
print('---------------------------------------------------------------')
print(axis_set)
print('---------------------------------------------------------------')

bulk_layer_number = len(axis_set)
setting=['T T T' for i in axis_set]

while True:
    print('Selected {}-Axis Coordinates'.format(abc_select))
    print('---------------------------------------------------------------')
    for i in range(len(axis_set)):
        print('{} : {} {}'.format(i,axis_set[i],setting[i]))
    print('---------------------------------------------------------------')
    
    user_select=input('Input number for Setting False (Finish : q) : ')
    
    if user_select=='q':
        break
    
    try:
        user_select=int(user_select)
        setting[user_select]='F F F'
    except:
        print('Input must be Int.')
    

    
for i in coordi:
    if abc_select=='a':
        ind=axis_set.index(i[0])
        i.append(setting[ind])
    elif abc_select=='b':
        ind=axis_set.index(i[1])
        i.append(setting[ind])
    elif abc_select=='c':
        ind=axis_set.index(i[2])
        i.append(setting[ind])


new_text_content=''

with open('POSCAR','r') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        
        if i==dc:
            new_string = sd+l.strip()
 
        elif i > dc and 'checkpoint' in globals():
            if checkpoint+dc+1 > i:
                new_string = '{} {} {} {}'.format(coordi[i-dc-1][0],coordi[i-dc-1][1],coordi[i-dc-1][2],coordi[i-dc-1][3])
            
        elif i > dc and 'checkpoint' not in globals():
            new_string = '{} {} {} {}'.format(coordi[i-dc-1][0],coordi[i-dc-1][1],coordi[i-dc-1][2],coordi[i-dc-1][3]) 
  
        else:
            new_string = l.strip()

        if new_string:
            new_text_content += new_string + '\n'
        else:
            new_text_content += '\n'

with open('POSCAR','w') as f:
    f.write(new_text_content)
    
print('Output Coordinates')
print('---------------------------------------------------------------')
print(new_text_content)
print('---------------------------------------------------------------')

print('POSCAR_Slab is Written!')
