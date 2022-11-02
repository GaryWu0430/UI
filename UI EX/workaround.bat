adb wait-for-device
adb root
adb remount
adb push workaround/fibocom_enable_suspend.sh /factory/factory/combo/
adb push workaround/target_led_switch.sh /factory/factory/combo/
adb push workaround/quanta_touch_fw_upgrade.sh /factory/factory/combo/
adb push workaround/ILI2882N00060H00_0x0C_AP_0x01_MP_AUO_0xFFFF_20220610.hex /factory/factory/combo/
adb push workaround/sp_tester /system/bin
adb shell chmod a+x /system/bin/sp_tester

adb shell chmod a+x /factory/factory/combo/*
