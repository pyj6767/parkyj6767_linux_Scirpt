import os
import warnings
from pymatgen.core import surface
from pymatgen.core import structure
from pymatgen.core import lattice
from pymatgen.core import sites
from array import *

#1. Class Structure from CONTCAR
File=input('Bulk structure 파일 이름을 작성 해주세요: ')
initial_structure=structure.Structure.from_file(f'{os.getcwd()}/{File}')

#2. Slabgenerator 관련 옵션 설정
miller_index=list(input('Slab 을 만들 Plane 의 Miller index h k l 을 작성해주세요 ex) 104: '))
miller_index=list(map(int, miller_index))

in_unit_planes=True #Layer 개수를 통한 Slab height 조절 사용
    
min_slab_size=float(input('Slab 의 최소 크기를 hkl Plane 개수로 입력해주세요: '))

Vacuum_height=float(input('Vacuum Height 를 Angstrom 단위로 입력해주세요: '))

lll_reduce=input('Slabs의 orthogonalization(LLL_reduce) 여부를 결정해주세요 ex) T/F(Default): ')
if lll_reduce=="" or lll_reduce=="F":
    lll_reduce=False
if lll_reduce=="T":
    lll_reduce=True
        
center_slab=input('Full-cell 을 만들지 Half-cell을 만들지 결정해주세요 ex) T(Full)/F(Half,Default): ')
if center_slab=="" or center_slab=="F":
	center_slab=False
if center_slab=="T":
    center_slab=True
    
primitive=input('slab을 Primitive cell 로 생성할지 말지 결정해주세요 ex)T(Default)/F: ')
if primitive=="" or primitive=="T":
	primitive=True
if primitive=="F":
    primitive==False
    
max_normal_search=input('Slab 생성시, c-axis 가 표면에 가능한 수직하도록 할 것인지(Maximally orthogonalized V3) 결정해주세요 ex) None(OFF, Default)/+int>(ON): ')
try:
	max_normal_search=int(max_normal_search)
except:
	max_normal_search=None
    
reorient_lattice=input('C-axis 가 Lattice 의 세번째 벡터가 되도록 Lattice parameters 를 재조정할지 결정해주세요 ex) T(Default)/F: ')
if reorient_lattice=="" or reorient_lattice=="T":
	reorient_lattice=True
if reorient_lattice=="F":
    reorient_lattice=False
    
#3. Slab 옵션을 바탕으로 Slab Class 의 생성
SlabGen=surface.SlabGenerator(initial_structure,miller_index, min_slab_size, 4, lll_reduce, center_slab, in_unit_planes, primitive, max_normal_search, reorient_lattice)
print('1. Raw slab class is generated\n-------------------------------------------------------------------------------------------------------------------------------')

#5. Slab class 에서 가능한 모든 Terminations 의 Slabs 를 생성(Symmetrize 기능 포함)
Slabs=SlabGen.get_slabs(None, 0.1,0.1,False,False,False)
print('2. All raw slab terminologies are generated\n')
        
Num=0
for i in Slabs:        
    print(i)
    #6. Slab Height 구하기
    MinC,MaxC=surface.get_slab_regions(i)[0] #Slab 영역의 C-coordinate 최소/최대를 출력
    Caxis=i.as_dict()['lattice']['c']
    Slab_Height=(MaxC-MinC)*Caxis
    print(f'3. Slab height Calcutated: {Slab_Height}\n')
   
    #5. Lattice from Slab Class -> Vacuum height 수정
    Slab_Temp=i.as_dict()
    C_OriLen=Slab_Temp['lattice']['c']
    C_NewLen=float(Slab_Height+Vacuum_height)
    Slab_Temp['lattice']['matrix'][2][0]=(C_NewLen/C_OriLen)*Slab_Temp['lattice']['matrix'][2][0] #Angstrom 기반의 Vacuum Height 재설정
    Slab_Temp['lattice']['matrix'][2][1]=(C_NewLen/C_OriLen)*Slab_Temp['lattice']['matrix'][2][1] #Angstrom 기반의 Vacuum Height 재설정
    Slab_Temp['lattice']['matrix'][2][2]=(C_NewLen/C_OriLen)*Slab_Temp['lattice']['matrix'][2][2] #Angstrom 기반의 Vacuum Height 재설정
    C_ratio=float(C_OriLen/C_NewLen) #이동시켜야할 C axis 비율 저장

    #6. Sites 의 C coordination 수정
    if center_slab: #Full Cell 의 경우
        for j in range(0,len(Slab_Temp['sites'])):
            Old_C=Slab_Temp['sites'][j]['abc'][2]
            New_C=0.5+((Old_C-0.5)*C_ratio)
            Slab_Temp['sites'][j]['abc'][2]=New_C

        #10. Slab 구조의 Output 파일이름 설정
        miller_index=list(map(str, miller_index))
        Structure_Name=f"{''.join(miller_index)}_Full_SNum{int(min_slab_size)}_VAng{int(Vacuum_height)}"
        
    else: #Half_Cell 의 경우
        for j in range(0,len(Slab_Temp['sites'])):
            Old_C=Slab_Temp['sites'][j]['abc'][2]
            New_C=Old_C*C_ratio
            Slab_Temp['sites'][j]['abc'][2]=New_C
        
        #10. Slab 구조의 Output 파일이름 설정
        miller_index=list(map(str, miller_index))
        Structure_Name=f"{''.join(miller_index)}_Half_SNum{int(min_slab_size)}_VAng{int(Vacuum_height)}"
            
    #11. 수정된 Dict 를 가지고 Slab 재 생성
    Slab_Final=surface.Slab.from_dict(Slab_Temp)
    Slab_Final=Slab_Final.get_sorted_structure(None,False)
    print(Slab_Final)
    
    #12. 생성된 Slabs의 정보 출력
    #with open(f"info_{Structure_Name}_#{Num}",'w') as f:
    #    f.write(f"------------{Structure_Name}_#{Num}----------------\n")
    #    f.write(str(Slab_Final))
    #    f.write(f"\nSurface area: {i.surface_area}")
    #    f.write(f"\nSlab height: {Slab_Height}")
    #    if i.is_polar():
    #        f.write(f"\nPolarization: Polar")
    #        f.write(f"\nDipole: {i.dipole}")
    #        #i.symmetrically_add_atom(specie, point, coords_are_cartesian=False)
    #    else:
    #        f.write(f"\nPolarization: non-Polar")
    #    if i.is_symmetric():
    #        f.write(f"\nInversion symmetry: Yes")
    #    else:
    #        f.write(f"\nInversion symmetry: No")
    #    if i.have_equivalent_surfaces():
    #        f.write(f"\n# of eqivalent sites on both surfaces: Same")
    #    else:
    #        f.write(f"\n# of eqivalent sites on both surfaces: Dif")
    
    #13. Slab 구조 파일의 생성
    structure.IStructure.to(Slab_Final,"poscar",filename=f"POSCAR_{Structure_Name}_#{Num}")
    
    Num=Num+1

