#!/bin/bash
#Production Program
#variables
CPU_TEST_TIME=3s
V33_HIGH=4
V33_LOW=2
V_BAT_HIGH=4
V_BAT_LOW=2
CPU_TEMP_HIGH=85
#funcions
function get_number() {
  sed 's/[^.0-9]//g' <<< $1
}

func(){
        LINE="---------------------"
        if [ $1 == "P" ];
        then
                echo "$LINE [$2 STATUS PASS!] $LINE"
        else
                echo "$LINE [$1 STATUS FAIL!] $LINE"
        fi
        return 1
}

#Test CPU and memory for 60s
echo -e "\n"
echo -e "Test CPU and Memory for ${CPU_TEST_TIME}"
uptime > uptime.txt
stress-ng --cpu 4 --vm 2 --vm-bytes 2000M --timeout $CPU_TEST_TIME
uptime >> uptime.txt
sensors > sensors.txt
#verify 3.3V status
V33=$(cat sensors.txt | grep 3.3V | awk '{print$2}')
V33_STATUSL=$(echo "$V33 > $V33_LOW "| bc)
V33_STATUSH=$(echo "$V33 < $V33_HIGH" | bc)
if [ "$V33_STATUSL" = "1" ] && [ "$V33_STATUSH" = "1" ];
then
	func P V33
else
	func V33
fi

#verify Vbat status
VBAT=$(cat sensors.txt | grep Vbat | awk '{print$2}')
VBAT_STATUSL=$(echo "$VBAT > $V_BAT_LOW" | bc)
VBAT_STATUSH=$(echo "$VBAT < $V_BAT_HIGH" | bc)
if [ "$VBAT_STATUSL" = "1" ] && [ "$VBAT_STATUSH" = "1" ];
then
	func P VBAT
else
	func VBAT
fi

#verify CPU status
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
	fi

#Test network
#declare -i index=1
#for ((;1;));
#do
#	echo -e "After insert Lan cord"
#	echo -e "Press 'y' to start network test"
#	read -n 1 k <&1
#	if [[ $k = 'y' ]];
#	then
#		echo -e "\nStarting network test\n"
#		ping 8.8.8.8 -c 5 >> ping.txt
#		NETWORK_STATUS=$(echo $?)
#		if [ "$NETWORK_STATUS" = "0" ];
#		then
#			func P "Port $index"
#		else
#			func Network
#		fi
#                index+=1
#       else
#	       continue
#       fi
#       if [[ $index > 4 ]];
#       then
#	       break
#       else
#	       continue
#
#       fi
#done

#Test wifi
echo "Test Wifi"
ifconfig > network.txt
WIFI_STATUS=$(cat network.txt | grep wl | awk -F, '/flags/{print$2}')
echo $WIFI_STATUS

if [ $WIFI_STATUS != "RUNNING" ];
then
	func P WIFI
else 
	func WIFI
fi

#Test comport
echo -e "Test COM1"
./send_tty.sh "1" /dev/ttyS0 > com1.txt 
COM1_STATUS=$(cat com1.txt | grep 1)
#echo $COM1_STATUS
if [ "$COM1_STATUS" = "1" ];
then
	func P COM1
else
	func COM1
fi
echo -e "Test COM2"
./send_tty.sh "1" /dev/ttyS1 > com2.txt
COM2_STATUS=$(cat com2.txt | grep 1)
if [ "$COM2_STATUS" = "1" ];
then
	func P COM2
else
	func COM2
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
fi	

echo "Test COM4"
./send_tty.sh "1" /dev/ttyS3 > com4.txt
COM4_STATUS=$(cat com4.txt | grep 1)
if [ "$COM4_STATUS" = "1" ];
then
        func P COM4
else
        func COM4
fi



#Test RS485 port
#echo "1" > /dev/ttyS2
#./rs485_port3.sh
#sleep 3
#echo "1" > /dev/ttyS3
#./rs485_port4.sh
#sleep 3

#Test onboard Lan


