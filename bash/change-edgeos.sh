#!/bin/bash
dir=`dirname $0`

hosts=()
while IFS= read -r line || [[ "$line" ]];  do 
	hosts+=("$line")
done < $dir/hosts.txt

echo "${hosts[@]}"

read -p "Username: " username

while true; do
	read -s -p "Password: " pass
	echo
	read -s -p "Confirm: " confirmed
	echo

	if [ "$pass" == "$confirmed" ]
	then
		break;
	else
		echo "Passwords don't match"
		echo
	fi
done

for hostname in "${hosts[@]}"; do 
	echo "Trying host: $hostname"
	echo
	sshpass -p "$pass" ssh -o StrictHostKeyChecking=no ${username}@${hostname} /bin/vbash  < $dir/commands
	echo "$hostname connection closed"
	echo 
done