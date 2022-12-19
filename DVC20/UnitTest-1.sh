#!/bin/bash
#Production Program
#---------------------------- Test Format ------------------------
date +"%F %T" > TIME.txt

Model="T20"
FORM+=Model,

#variables
CPU_TEST_TIME=2s
V33_HIGH=4
V_BAT_HIGH=4
V_BAT_LOW=2
CPU_TEMP_HIGH=85

function get_number() {
  sed 's/[^.0-9]//g' <<< $1
}

func(){
	LINE="---------------------"
	if [ $1 == "P" ];
	then
		echo "$LINE [$2 STATUS PASS!] $LINE"
		echo "$2:0" >> REPORT.txt
	else
		echo "$LINE [$1 STATUS FAIL!] $LINE"
		echo "$1:1" >> REPORT.txt
	fi
	return 1
}


main(){
	#------------------- 

	echo -n "Enter BARCODE: "
	read BARCODE
	echo "Your BARCODE is $BARCODE"

	>REPORT.txt
	echo "Start Testing"
	start=$SECONDS

	#-------------------- Test CPU and memory for 60s -----------------------
	echo -e "\n"
	echo -e "Test CPU and Memory for ${CPU_TEST_TIME}"
	uptime > uptime.txt
	stress-ng --cpu 4 --vm 2 --vm-bytes 2000M --timeout $CPU_TEST_TIME
	uptime >> uptime.txt
	sensors > sensors.txt
	#verify 3.3V status
	V33=$(cat sensors.txt | grep 3.3V | awk '{print$2}')
	V33_status=$(echo "$V33 < $V33_HIGH "| bc)
	if [ "$V33_status" = "1" ];
	then
		func P V33
	else
		func V33
		return 1
	fi

	#--------------------- verify Vbat status -------------------------
	VBAT=$(cat sensors.txt | grep Vbat | awk '{print$2}')
	VBAT_STATUSL=$(echo "$VBAT > $V_BAT_LOW" | bc)
	VBAT_STATUSH=$(echo "$VBAT < $V_BAT_HIGH" | bc)
	if [ "$VBAT_STATUSL" = "1" ] && [ "$VBAT_STATUSH" = "1" ];
	then
		func P Vbat
	else
		func Vbat
		return 1
	fi

	#---------------------- verify CPU status ------------------------
	CPU_TEMPS_UNIT=$(cat sensors.txt | grep Core | awk '{print$3}')
	#echo $CPU_TEMPS_UNIT

	for CPU_TEMP in $CPU_TEMPS_UNIT;
	do
		CPU_TEMP=$(get_number $CPU_TEMP)

		CPU_TEMP_STATUS=$(echo "$CPU_TEMP < $CPU_TEMP_HIGH" | bc)
	done
		if [ "$CPU_TEMP_STATUS" = "1" ];
		then
			func P "CPU TEMP"
		else
			func "CPU TEMP"
			return 1
		fi



: << EOF

	#----------------------- Verify LAN PORT -----------------------------
	#LAN_PORT=("172.17.99.99" "172.17.99.100" "172.17.99.101" "172.17.99.102")
	#len=${#LAN_PORT[@]}
	declare -i index=1

	for ((;1;));
	do
		#echo ${LAN_PORT[$i]}
		#ping ${LAN_PORT[$i]} -c 5
		echo -e "Press 'y' to start network test"


		read -n 1 k <&1
		if [[ $k = y ]]; then
			echo -e "\nStarting NETWORK Test\n"
			ping 8.8.8.8 -c 1 >> ping.txt
			NETWORK_STATUS=$(echo $?)
			#echo $NETWORK_STATUS
			if [ "$NETWORK_STATUS" = "0" ];
			then
				func P "Port $index"
			else
				func Network
				break
			fi
			#echo -e "Finished $index\n"
			index+=1
		else
			continue
			
		fi


		if [[ $index>4 ]]; then
			break
		else
			continue
		fi

	done
	duration=$(( SECONDS - start ))
	echo -e "Test Time: $duration s"
	echo $duration >> TIME.txt




	#------------------------ wifi -------------------------
	iwconfig > wifi.txt
	t1=`cat wifi.txt | grep "ESSID" | awk '{print$4}'`

	if [ $t1 != "ESSID:off/any" ]; then
		func P WIFI
	else
		func WIFI
		return 1
	fi
EOF

	#---------------------- Network ------------------------------
	ifconfig -s > NET.txt
	LAN_PORT=("eno1" "enp2s0" "enp6s0" "enp7s0")
	len=${#LAN_PORT[@]}

	for (( i=0; i<len; i++ ))
	do
		NET=$(ifconfig -s | grep ${LAN_PORT[$i]} | awk '{printf$11}')
		#WIFI=$(ifconfig -s | grep wlp1s0 | awk '{printf$11}')
		echo -e $NET
	done


	#--------------------- Duration Time --------------------------
	duration=$(( SECONDS - start ))
	echo -e "Test Time: $duration s"
	echo $duration >> TIME.txt
}
#---------------------- main function ------------------------
main
#---------------------- Pass/Fail Criteria -------------------
criteria(){
	declare -i index=1

	echo -e "START read lines"
	while read rows
	do 
		OLF_IFS="$IFS"
		IFS=":"
		array=($rows)
		IFS="$OLD_IFS"
		
		echo $array 

		for i in ${array[@]}
		do
			if [ $(($index%2)) = 0 ]; 
			then
				echo $i
			fi
			index+=1
		done
		
	done < REPORT.txt
}
criteria


#---------------------- Upload Data --------------------------
#python3 POST-DATA.py
