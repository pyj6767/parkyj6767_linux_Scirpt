#!/usr/bin/env python3.9
#Script Name : Latinc | Made by Young-Jun Park, yjpark29@postech.ac.kr
#Description
#: Lattice Parameter a축으로 0.1씩 늘려가는/줄여가는 코드(Uncompleted, If want axis change, we should edit this code
#: Sub Script for Latin

import sys
import numpy as np

if len(sys.argv) == 2:
    inc=float(sys.argv[1])

POSCARfile = open('POSCAR','r')

linedata=POSCARfile.readlines()

DC=linedata[7] #Direct / Cartesian

Lattice_Parameters=linedata[2:5]
coordinates=linedata[8:]

LP=[]
coordi=[]

#LP 추출
for i in range(0, len(Lattice_Parameters)):
    Lattice_Parameters[i]=Lattice_Parameters[i].replace('\n','').replace('\r','')
    LP.append(Lattice_Parameters[i].split(' '))
    
for j in range(0, len(LP)):
    LP[j] = [float(k) for k in LP[j] if k != '']

print(LP)

#좌표 추출
for i in range(0, len(coordinates)):
    coordinates[i]=coordinates[i].replace('\n','').replace('\r','')
    coordi.append(coordinates[i].split(' '))
    
for j in range(0, len(coordi)):
    coordi[j] = [float(k) for k in coordi[j] if k != '']

print(coordi)

#lattice Parameter 늘려가기
#inc=float(input('Increment(Decrese : Minus) : '))

#LP[0][0]=LP[0][0]+inc
LP[1][1]=LP[1][1]+inc
    
new_text_content=''
    
with open('POSCAR','r') as f:
    lines=f.readlines()
    for i, l in enumerate(lines):
        if i==3:
            new_string='{} {} {}'.format(LP[i-2][0], LP[i-2][1], LP[i-2][2])
        else:
            new_string = l.strip()
        if new_string:
            new_text_content += new_string + '\n'
        else:
            new_text_content += '\n'
            
with open('POSCAR', 'w') as f:
    f.write(new_text_content)
