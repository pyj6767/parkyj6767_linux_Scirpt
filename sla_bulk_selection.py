#!/usr/bin/env python
#Script Name : bulk_selection.py
#Description
#: Bulk Layer Selection for Slab
#: Sub Script for slayer

import sys
import numpy as np
import pandas as pd

if len(sys.argv) == 3:
    abc_select=int(sys.argv[1])
    bulk_layer_number=int(sys.argv[2])

elif len(sys.argv) > 3:
    print('Number of Argument must be 1 !')
    quit()

elif len(sys.argv) <= 2:
    print('Argument Error')
    quit()

if abc_select=='1':
    abc_select='a'
elif abc_select=='2':
    abc_select='b'
else:
    abc_select='c'

POSCARfile = open('POSCAR_Slab','r')

linedata=POSCARfile.readlines()

for i in range(len(linedata)):
    if linedata[i].find('Direct')>-1:
        dc=i
    elif linedata[i].find('Cartesian')>-1:
        dc=i

coordinates=linedata[dc+1:]

coordi=[]
for i in range(len(coordinates)):
    coordinates[i]=coordinates[i].replace('\n','').replace('\r','')
    coordi.append(coordinates[i].split(' '))

for j in range(len(coordi)):
    coordi[j] = [k for k in coordi[j] if k != '']
    
for p in range(len(coordi)):
    if len(coordi[p])>3:
        coordi[p]=coordi[p][0:3]

for y in range(len(coordi)):
    coordi[y] = [float(u) for u in coordi[y]]

#abc_select=input('Select Slab Axis (a,b,c) : ')

axis_set=[]
for i in coordi:
    if abc_select=='a':
        axis_set.append(i[0])
    elif abc_select=='b':
        axis_set.append(i[1])
    elif abc_select=='c':
        axis_set.append(i[2])

axis_set=list(set(axis_set))
axis_set.sort()

print('Net {}-Axis Coordinates'.format(abc_select))
print('---------------------------------------------------------------')
print(axis_set)
print('---------------------------------------------------------------')

if len(axis_set)%2==1:
    oe='odd'
elif len(axis_set)%2==0:
    oe='even'

while True:
    #bulk_layer_number = int(input('Number of Bulk Layer : '))
    print('---------------------------------------------------------------')

    if ( bulk_layer_number%2==1 and oe=='even' ) or ( bulk_layer_number%2==0 and oe=='odd' ):
        print('---------------------------------------------------------------')
        print('You Should Matching Odd/Even Number with Total Layer Number(=>{})'.format(oe))
        print('---------------------------------------------------------------')
    else:
        break


while len(axis_set)!=bulk_layer_number:
    axis_set.pop()
    axis_set.reverse()
    axis_set.pop()
    axis_set.reverse()
    
print('Selected {}-Axis Coordinates'.format(abc_select))
print('---------------------------------------------------------------')
print(axis_set)
print('---------------------------------------------------------------')
    
for i in coordi:
    if abc_select=='a':
        if i[0] in axis_set:
            i.append('F F F')
        elif i[0] not in axis_set:
            i.append('T T T')
    elif abc_select=='b':
        if i[1] in axis_set:
            i.append('F F F')
        elif i[1] not in axis_set:
            i.append('T T T')
    elif abc_select=='c':
        if i[2] in axis_set:
            i.append('F F F')
        elif i[2] not in axis_set:
            i.append('T T T')

print('Output Coordinates')
print('---------------------------------------------------------------')
print(coordi)
print('---------------------------------------------------------------')


new_text_content=''

with open('POSCAR_Slab','r') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        if i > dc:
            new_string = '{} {} {} {}'.format(coordi[i-dc-1][0],coordi[i-dc-1][1],coordi[i-dc-1][2],coordi[i-dc-1][3])
        else:
            new_string = l.strip()

        if new_string:
            new_text_content += new_string + '\n'
        else:
            new_text_content += '\n'

with open('POSCAR_Slab','w') as f:
    f.write(new_text_content)
