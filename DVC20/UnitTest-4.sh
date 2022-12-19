#!/bin/bash
#Production Program
#---------------------------- Test Format ------------------------
echo "DVC20" > TIME.txt

#variables
CPU_TEST_TIME=10s
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
	#------------------- pre-processing -------------------------------------

	echo -n "Enter BARCODE: "
	read BARCODE
	echo "Your BARCODE is $BARCODE"
	echo $BARCODE >> TIME.txt

	>REPORT.txt
	echo "Start Testing"
	start=$SECONDS
	date +"%F %T" >> TIME.txt
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
			func P CPU
		else
			func CPU
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




	#---------------------- COM Port -----------------------------
	echo -e "Test COM1"
	./send_tty.sh "1" /dev/ttyS0 > com1.txt 
	COM1_STATUS=$(cat com1.txt | grep 1)
	#echo $COM1_STATUS
	if [ "$COM1_STATUS" = "1" ];
	then
		func P COM1
	else
		func COM1
		return 1
	fi
	
	echo -e "Test COM2"
	./send_tty.sh "1" /dev/ttyS1 > com2.txt
	COM2_STATUS=$(cat com2.txt | grep 1)
	if [ "$COM2_STATUS" = "1" ];
	then
		func P COM2
	else
		func COM2
		return 1
	fi

	#test RS232
	echo "Test COM3"
	./send_tty.sh "1" /dev/ttyS2 > com3.txt
	COM3_STATUS=$(cat com3.txt | grep 1)
	if [ "$COM3_STATUS" = "1" ];
	then 
		func P COM3
	else 
		func COM3
		return 1
	fi	

	echo "Test COM4"
	./send_tty.sh "1" /dev/ttyS3 > com4.txt
	COM4_STATUS=$(cat com4.txt | grep 1)
	if [ "$COM4_STATUS" = "1" ];
	then
	        func P COM4
	else
	        func COM4
		return 1
	fi

	#---------------------- Network ------------------------------
	ifconfig -s > NET.txt
	LAN_PORT=("eno1" "enp2s0" "enp6s0" "enp7s0")
	len=${#LAN_PORT[@]}

	for (( i=0; i<len; i++ ))
	do
		NET=$(ifconfig -s | grep ${LAN_PORT[$i]} | awk '{printf$11}')
		
#		echo -e $[i+1] $NET
		if [ $NET = "BMRU" ]; then
			func P "PORT$[i+1]"
		
		else
			func "PORT$[i+1]"
			return 1
		fi
	done

	#--------------------- WIFI ----------------------------------
	WIFI=$(ifconfig -s | grep wlp1s0 | awk '{printf$11}')
	if [ $WIFI = "BMRU" ]; then
		func P "WIFI"
	else
		func WIFI
		return 1
	fi
}

#---------------------- main function ------------------------
main

#--------------------- Duration Time --------------------------
duration=$(( SECONDS - start ))
echo -e "Test Time: $duration s"
echo $duration >> TIME.txt


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
python3 POST-DATA.py
