#!/bin/bash
#++ execute during first boot

default_nameserver=$(cat /etc/resolv.conf 2>/dev/null | awk '/^domain/ { print $2 }')
default_domain=$(sed 's/[^.]*\.\([^.]*\)\..*/\1/' <<< "${default_nameserver}")
device_os=$(defaults read "/System/Library/CoreServices/SystemVersion" ProductVersion)	# 10.9 etc
device_build=$(defaults read "/System/Library/CoreServices/SystemVersion" ProductBuildVersion) # 13A603 etc
device_serial=$(ioreg -c IOPlatformExpertDevice | sed -E -n -e '/IOPlatformSerialNumber/{s/^.*[[:space:]]"IOPlatformSerialNumber" = "(.+)"$/\1/p;q;}')
[ $(networksetup -getMACADDRESS en1 | awk '{print $3}' | sed s/://g) == "The" ] && device_interface="en1" || device_interface="en0"  # wifi nic if eth0 is empty (mac book air etc)
device_macaddress=$(networksetup -getMACADDRESS ${device_interface} | awk '{print $3}' | sed s/://g) # minus : chars
device_model=$(/usr/sbin/ioreg -rd1 -c IOPlatformExpertDevice | grep -E model | awk '{print $3}' | sed 's/\<\"//' | sed 's/\"\>//')
device_ram=$(/usr/sbin/system_profiler SPHardwareDataType | grep "Memory" | awk '{print $2$3}')
device_cpu=$(/usr/sbin/system_profiler SPHardwareDataType | grep "Processor Name" | awk '{print $3$4$5$6$7$8$9}')
device_en0=$(/usr/sbin/ipconfig getifaddr en0)
device_en1=$(/usr/sbin/ipconfig getifaddr en1)
device_fw1=$(/usr/sbin/ipconfig getifaddr fw1)
device_utun0=$(ifconfig | grep -A1 'utun0' | grep -A1 'inet' | awk '{print $2}')
formatted_date=$(date +"%Y%m%d%H%M%S")

#++ just an example for now
#++ your code goes here

#++ disable gatekeeper
/usr/sbin/spctl --master-disable

#++ set a name for troubleshooting/locating
scutil --set ComputerName "${device_macaddress}"
scutil --set LocalHostName "${device_macaddress}"
scutil --set HostName "${device_macaddress}"
hostname "${device_macaddress}"

#++ reset loginwindow
defaults delete "${path_root}/System/Library/LaunchDaemons/com.apple.loginwindow.plist" ProgramArguments
defaults write "${path_root}/System/Library/LaunchDaemons/com.apple.loginwindow.plist" ProgramArguments -array-add "/System/Library/CoreServices/loginwindow.app/Contents/MacOS/loginwindow" "console"
chown root:wheel "${path_root}/System/Library/LaunchDaemons/com.apple.loginwindow.plist"
chmod 644 "${path_root}/System/Library/LaunchDaemons/com.apple.loginwindow.plist"

#++ should not get here again
reboot

exit 0
