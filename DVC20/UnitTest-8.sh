#!/bin/bash

#---------------------------- Test Format ------------------------
echo "DVC20" > TIME.txt

#variables
CPU_TEST_TIME=1s
V33_HIGH=4
V33_LOW=2
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

iWantPass(){
    echo -e "\033[32m #######      ####      ######     ######  \033[0m"
    echo -e "\033[32m ########    ######    ########   ######## \033[0m"
    echo -e "\033[32m ##    ##   ##    ##   ##     #   ##     # \033[0m"
    echo -e "\033[32m ##    ##   ##    ##    ###        ###     \033[0m"
    echo -e "\033[32m ########   ########     ####       ####   \033[0m"
    echo -e "\033[32m #######    ########       ###        ###  \033[0m"
    echo -e "\033[32m ##         ##    ##   #     ##   #     ## \033[0m"
    echo -e "\033[32m ##         ##    ##   ########   ######## \033[0m"
    echo -e "\033[32m ##         ##    ##    ######     ######  \033[0m"

}

iWantFail(){
    echo -e "\033[31m #######      ####     ########   ###      \033[0m"
    echo -e "\033[31m #######     ######    ########   ###      \033[0m"
    echo -e "\033[31m ##         ##    ##      ##      ###      \033[0m"
    echo -e "\033[31m ##         ##    ##      ##      ###      \033[0m"
    echo -e "\033[31m #######    ########      ##      ###      \033[0m"
    echo -e "\033[31m #######    ########      ##      ###      \033[0m"
    echo -e "\033[31m ##         ##    ##      ##      ###      \033[0m"
    echo -e "\033[31m ##         ##    ##   ########   ######## \033[0m"
    echo -e "\033[31m ##         ##    ##   ########   ######## \033[0m"

}

main(){
	#------------------- pre-processing -------------------------------------
	echo -n "Enter Serial Number: "
	read BARCODE
	echo "Your Serial Number is $BARCODE"
	echo $BARCODE >> TIME.txt

	echo -n "Enter Work Order Number: "
	read WO
	echo "Your Work Order Number is $WO"
	echo $WO >> TIME.txt

	>REPORT.txt
	echo "Start Testing"
	start=$SECONDS
	date +"%F %T" >> TIME.txt


	#-------------------- Screen --------------------------------------------
	screen=$(xrandr | grep 3840x2160 | awk '{printf$2}')
	if [ $screen = "connected60.00*+" ];
	then
		func P Screen
	else
		func Screen
		iWantFail
		return 1
	fi

	#-------------------- eMMC Check ----------------------------------------
	eMMC=$(lsblk -s | grep -w mmcblk0boot0 | awk '{printf$1}')
	if [ $eMMC = 'mmcblk0boot0' ];
	then
		func P eMMC
	else
		func eMMC
		iWantFail
		return 1
	fi


	#-------------------- V33 Verify ------------------------------------
	#verify 3.3V status
	sensors > sensors.txt
	V33=$(cat sensors.txt | grep 3VSB | awk '{print$2}')
	V33_status_H=$(echo "$V33 < $V33_HIGH "| bc)
	V33_status_L=$(echo "$V33 > $V33_LOW "| bc)


	if [ "$V33_status_H" = "1" ] && [ "$V33_status_L" = "1" ];
	then
		func P V33
	else
		func V33
		iWantFail
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
		iWantFail
		return 1
	fi


	#---------------------- COM Port -----------------------------

	var=$(python3 ttyS0.py /dev/ttyS0)
	#echo -e $var
	if [ $var = "Pass" ]; then
		func P COM1
	else
		func COM1
		iWantFail
		return 1
	fi

	var=$(python3 ttyS0.py /dev/ttyS1)
        #echo -e $var
        if [ $var = "Pass" ]; then
                func P COM2
        else
                func COM2
		iWantFail
                return 1
        fi

	var=$(python3 ttyS0.py /dev/ttyS2)
        #echo -e $var
        if [ $var = "Pass" ]; then
                func P COM3
        else
                func COM3
		iWantFail
                return 1
        fi

	var=$(python3 ttyS0.py /dev/ttyS3)
        #echo -e $var
        if [ $var = "Pass" ]; then
                func P COM4
        else
                func COM4
		iWantFail
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
			func P "LAN$[i+1]"
		
		else
			func "LAN$[i+1]"
			iWantFail
			return 1
		fi
	done

	#--------------------- WIFI ----------------------------------
	WIFI=$(ifconfig -s | grep wlp1s0 | awk '{printf$11}')
	if [ $WIFI = "BMRU" ]; then
		func P "WIFI"
	else
		func WIFI
		iWantFail
		return 1
	fi
	


	#-------------------- Line Out-------------------------------------------
#: << EOF
	for ((;1;));
	do
		echo -e "Line Out Test [y/n]"
		read -n 1 k <&1
		if [[ $k = y ]]; then
			func P Audio
			break
		elif [[ $k = n ]]; then
			func Audio
			iWantFail
			return 1
		else
			continue
		fi
	done
#EOF


	#-------------------- Test CPU and memory for 60s -----------------------	
	stress-ng --cpu 4 --vm 2 --vm-bytes 2000M --timeout $CPU_TEST_TIME --log-brief
	stress-ng --cpu 4 --vm 2 --vm-bytes 2000M --timeout $CPU_TEST_TIME --metrics --log-brief

	echo -e "\n"
	echo -e "Test CPU and Memory for ${CPU_TEST_TIME}"
	uptime > uptime.txt
	stress-ng --cpu 4 --vm 2 --vm-bytes 2000M --timeout $CPU_TEST_TIME
	uptime >> uptime.txt
	
	#---------------------- verify CPU status ------------------------
	sensors > sensors.txt
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
			iWantFail
			return 1
		fi
		iWantPass
	}


#---------------------- main function ------------------------
main

#--------------------- Duration Time --------------------------
duration=$(( SECONDS - start ))
echo -e "Test Time: $duration s"
echo $duration >> TIME.txt

#---------------------- Pass/Fail Criteria -------------------
: << EOF
如果一台電腦有兩個以上的網路介面（例如多張網路卡），我們可以使用 -I 參數指定要測試的網路介面：
ping -I eth0 blog.gtwang.org

另外也可以使用 IP 位址來指定：
ping -I 45.118.135.69 blog.gtwang.org
EOF

#---------------------- Upload Data --------------------------
#ipython3 POST-DATA.py
