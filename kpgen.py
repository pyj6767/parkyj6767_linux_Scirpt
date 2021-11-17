#!/usr/bin/python
#Script Name kpgen.py
#Description
#: KPOINTS List based on Lattice Parameter

import sys

Dim_dict={1:'1D',2:'2D',3:'3D'}

if len(sys.argv) == 3:
    numbers=int(sys.argv[1])
    Dimension=int(sys.argv[2])

elif len(sys.argv) > 3:
    print('Number of Argument must be 1 !')
    quit()

elif len(sys.argv) == 2:
    numbers=int(input('Input number of kpt for Generation : '))
    print('-------------------------------------------------------')
    print(Dim_dict)
    print()
    Dimension=int(input('Input Dimension Of Your Structure : '))
    print('-------------------------------------------------------')

Dimension=Dim_dict[Dimension]
    
POSCARfile = open('POSCAR','r')

linedata=POSCARfile.readlines()

if Dimension=='3D':
    linedata=linedata[2:5]

    Lattice_Parameter=[]
    for i in range(0, len(linedata)):
        linedata[i]=linedata[i].replace('\n','').replace('\r','')
        Lattice_Parameter.append(linedata[i].split(' '))

    for j in range(0, len(Lattice_Parameter)):
        Lattice_Parameter[j] = [k for k in Lattice_Parameter[j] if k != '']

    for k in range(0,len(Lattice_Parameter)):
        Lattice_Parameter[k] = sum([float(num)*float(num) for num in Lattice_Parameter[k]])**(0.5)

    Reciprocal=[]

    for m in range(0,len(Lattice_Parameter)):
        Reciprocal.append(1/Lattice_Parameter[m])

    minvalue=min(Reciprocal)

    for n in range(0, len(Reciprocal)):
        Reciprocal[n]=Reciprocal[n]/minvalue

    kpt=[]
    for n in range(1,numbers+1):
        temp_kpt=[]
        for q in range(0, len(Reciprocal)):
            temp_kpt.append(round(Reciprocal[q]*n))
        kpt.append(temp_kpt)

    print('-------------------------------------------------------------------')
    print('Lattice Parameter : {} {} {}'.format(Lattice_Parameter[0],Lattice_Parameter[1],Lattice_Parameter[2]))
    print('-------------------------------------------------------------------')

elif Dimension=='2D':
    linedata=linedata[2:4]

    #Same with 3D Code
    #----------------------------------------------------------------------------------
    Lattice_Parameter=[]
    for i in range(0, len(linedata)):
        linedata[i]=linedata[i].replace('\n','').replace('\r','')
        Lattice_Parameter.append(linedata[i].split(' '))
    for j in range(0, len(Lattice_Parameter)):
        Lattice_Parameter[j] = [k for k in Lattice_Parameter[j] if k != '']
    for k in range(0,len(Lattice_Parameter)):
        Lattice_Parameter[k] = sum([float(num)*float(num) for num in Lattice_Parameter[k]])**(0.5)
    Reciprocal=[]
    for m in range(0,len(Lattice_Parameter)):
        Reciprocal.append(1/Lattice_Parameter[m])
    minvalue=min(Reciprocal)
    for n in range(0, len(Reciprocal)):
        Reciprocal[n]=Reciprocal[n]/minvalue
    kpt=[]
    for n in range(1,numbers+1):
        temp_kpt=[]
        for q in range(0, len(Reciprocal)):
            temp_kpt.append(round(Reciprocal[q]*n))
        temp_kpt.append(1) #For 2D Strcuture
        kpt.append(temp_kpt)
    #------------------------------------------------------------------------------------
        
    print('-------------------------------------------------------------------')
    print('Lattice Parameter : {} {} {}'.format(Lattice_Parameter[0],Lattice_Parameter[1],'C:2D Structure'))
    print('-------------------------------------------------------------------')
    
elif Dimension=='1D':
    linedata=linedata[2:3]

    #Same with 3D Code
    #----------------------------------------------------------------------------------
    Lattice_Parameter=[]
    for i in range(0, len(linedata)):
        linedata[i]=linedata[i].replace('\n','').replace('\r','')
        Lattice_Parameter.append(linedata[i].split(' '))
    for j in range(0, len(Lattice_Parameter)):
        Lattice_Parameter[j] = [k for k in Lattice_Parameter[j] if k != '']
    for k in range(0,len(Lattice_Parameter)):
        Lattice_Parameter[k] = sum([float(num)*float(num) for num in Lattice_Parameter[k]])**(0.5)
    Reciprocal=[]
    for m in range(0,len(Lattice_Parameter)):
        Reciprocal.append(1/Lattice_Parameter[m])
    minvalue=min(Reciprocal)
    for n in range(0, len(Reciprocal)):
        Reciprocal[n]=Reciprocal[n]/minvalue
    kpt=[]
    for n in range(1,numbers+1):
        temp_kpt=[]
        for q in range(0, len(Reciprocal)):
            temp_kpt.append(round(Reciprocal[q]*n))
        temp_kpt.append(1) #For 2D Strcuture
        temp_kpt.append(1) #For 2D Strcuture
        kpt.append(temp_kpt)
    #----------------------------------------------------------------------------------

    print('-------------------------------------------------------------------')
    print('Lattice Parameter : {} {} {}'.format(Lattice_Parameter[0],'B:1D Plane','C:2D Plane'))
    print('-------------------------------------------------------------------')
    
print('num | KPOINTS')
print('--------------')
for kp in range(0, len(kpt)):
    print('{}  :  {}  {}  {}'.format(kp+1,int(kpt[kp][0]),int(kpt[kp][1]),int(kpt[kp][2])))

if len(sys.argv) == 3:
    quit()
else:
    selection=int(input('Select KPOINTS : '))-1

new_text_content=''

with open('KPOINTS','r') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        if i == 3:
            new_string = '{} {} {}'.format(int(kpt[selection][0]),int(kpt[selection][1]),int(kpt[selection][2]))
        else:
            new_string = l.strip()

        if new_string:
            new_text_content += new_string + '\n'
        else:
            new_text_content += '\n'

with open('KPOINTS','w') as f:
    f.write(new_text_content)


