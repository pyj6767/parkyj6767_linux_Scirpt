#!/bin/sh
#Script Name : jhrun.sh | Made by Young-Jun Park, yjpark29@postech.ac.kr
#Description
#: Print Job History & Print run.sh
#Inspired by Kyung-Yeon Doh's and Hyeon Kim's jobinto Code

read -p "Enter the number of job history (anykey(default) = 5): " num

if [[ $num -lt 1 ]] || [[ $num == $String22 ]]
then
num=5
fi

jobid=`tail -$num  ~/a.log/input.log | tac | awk -F"." '{print $1}'`
jobaddre=`tail -$num ~/a.log/input.log | tac | awk '{print $2}'`
whattime=`tail -$num ~/a.log/input.log | tac | awk '{print "["$3"] "$4"/"$5"/"$6}' | sed -e 's/ //'`

#echo $jobid
#echo $jobaddre
#echo $whattime

echo "-------------------"
echo " [ `whoami` ]"
echo "-------------------"
#echo " Num        Date, Time         JobID                           Address"
#echo "=====||======================||=======||======================================================"
#for i in $(seq $num)
#do

#timelist=`echo $whattime | awk '{print $'"$i"'}'`
#idlist=`echo $jobid | awk '{print $'"$i"'}'`
#addlist=`echo $jobaddre | awk '{print $'"$i"'}'`

#echo " " $i  " ||" $timelist  "||"  $idlist  "||" $addlist

#done
echo "=============================================================================================="
for i in $(seq $num)
do
dir_name=`echo $jobaddre | awk '{print $'"$i"'}'`

if [ -e $dir_name/run.sh ]; then
echo "Directory : "$dir_name
echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
head -4 $dir_name/run.sh
echo "-------------------------------------------------------------------------------------------"

else
echo "Directory : "$dir_name
echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
echo "There is No run.sh file."
echo "-------------------------------------------------------------------------------------------"


fi


done
echo "==========================================================================================="



exit 0

