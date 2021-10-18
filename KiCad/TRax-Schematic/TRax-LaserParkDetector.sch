EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 3 3
Title "TRax Modules"
Date "2021-09-19"
Rev "v1.1"
Comp "Robert Ferguson Observatory"
Comment1 "David Kensiski"
Comment2 ""
Comment3 ""
Comment4 "v1.1 adds detector inverter/isolator; add fob module"
$EndDescr
$Comp
L Regulator_Linear:LM1084-ADJ U9
U 1 1 60D50131
P 2050 4200
F 0 "U9" V 1900 3900 50  0000 L CNN
F 1 "LM1084" H 1900 4350 50  0000 L CNN
F 2 "" H 2050 4450 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm1084.pdf" H 2050 4200 50  0001 C CNN
	1    2050 4200
	0    -1   -1   0   
$EndComp
$Comp
L Regulator_Linear:LM1084-ADJ U11
U 1 1 60D51913
P 4750 3800
F 0 "U11" V 4796 3905 50  0000 L CNN
F 1 "LM1084" V 4500 3450 50  0000 L CNN
F 2 "" H 4750 4050 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm1084.pdf" H 4750 3800 50  0001 C CNN
	1    4750 3800
	0    -1   -1   0   
$EndComp
$Comp
L Connector:6P6C J16
U 1 1 60D52C37
P 2250 5350
F 0 "J16" V 2350 5000 50  0000 R CNN
F 1 "RJ25" V 2250 5000 50  0000 R CNN
F 2 "" V 2250 5375 50  0001 C CNN
F 3 "~" V 2250 5375 50  0001 C CNN
	1    2250 5350
	0    -1   -1   0   
$EndComp
$Comp
L Connector:6P6C J17
U 1 1 60D54B92
P 4950 5350
F 0 "J17" V 5053 5020 50  0000 R CNN
F 1 "RJ25" V 4962 5020 50  0000 R CNN
F 2 "" V 4950 5375 50  0001 C CNN
F 3 "~" V 4950 5375 50  0001 C CNN
	1    4950 5350
	0    -1   -1   0   
$EndComp
$Comp
L Device:Laserdiode_1C2A LD1
U 1 1 60D6A971
P 5000 2300
F 0 "LD1" H 4950 2075 50  0000 C CNN
F 1 "Laser Diode" H 4950 2166 50  0000 C CNN
F 2 "" H 4900 2275 50  0001 C CNN
F 3 "~" H 5030 2100 50  0001 C CNN
	1    5000 2300
	-1   0    0    1   
$EndComp
Wire Wire Line
	2050 3900 2050 3850
$Comp
L Device:R R17
U 1 1 60D77FD1
P 2200 3850
F 0 "R17" V 1993 3850 50  0000 C CNN
F 1 "118" V 2084 3850 50  0000 C CNN
F 2 "" V 2130 3850 50  0001 C CNN
F 3 "~" H 2200 3850 50  0001 C CNN
	1    2200 3850
	0    1    1    0   
$EndComp
$Comp
L Device:R R18
U 1 1 60D78832
P 2500 3850
F 0 "R18" V 2293 3850 50  0000 C CNN
F 1 "354" V 2384 3850 50  0000 C CNN
F 2 "" V 2430 3850 50  0001 C CNN
F 3 "~" H 2500 3850 50  0001 C CNN
	1    2500 3850
	0    1    1    0   
$EndComp
Wire Wire Line
	2350 4200 2350 3850
Connection ~ 2350 3850
Connection ~ 2050 3850
NoConn ~ 2850 2650
$Comp
L Device:R R22
U 1 1 60D845F7
P 4900 3450
F 0 "R22" V 4650 3450 50  0000 C CNN
F 1 "118" V 4750 3450 50  0000 C CNN
F 2 "" V 4830 3450 50  0001 C CNN
F 3 "~" H 4900 3450 50  0001 C CNN
	1    4900 3450
	0    1    1    0   
$EndComp
Wire Wire Line
	4750 3500 4750 3450
Connection ~ 4750 3450
Wire Wire Line
	4750 2300 4800 2300
Wire Wire Line
	5300 2300 5350 2300
Wire Wire Line
	5350 2300 5350 3450
Wire Wire Line
	5050 3800 5050 3450
Connection ~ 5050 3450
Wire Wire Line
	4750 4950 4750 4100
Wire Wire Line
	5050 4950 5050 4150
Wire Wire Line
	5050 4150 5350 4150
Wire Wire Line
	5350 4150 5350 3450
Connection ~ 5350 3450
NoConn ~ 5150 4950
NoConn ~ 4950 4950
NoConn ~ 4850 4950
NoConn ~ 4650 4950
NoConn ~ 2450 4950
NoConn ~ 1950 4950
Text Notes 4600 3450 0    50   ~ 0
5V
Text Notes 2350 2900 0    50   ~ 0
5V
Wire Notes Line
	1650 1550 1650 5750
Wire Notes Line
	3800 5750 3800 1550
Wire Notes Line
	1650 5750 3800 5750
Wire Notes Line
	1650 1550 3800 1550
Wire Notes Line
	4350 5750 4350 1550
Wire Notes Line
	4350 1550 5550 1550
Wire Notes Line
	5550 1550 5550 5750
Wire Notes Line
	5550 5750 4350 5750
Text Notes 2200 1450 0    100  ~ 0
Park Detector
Text Notes 4500 1450 0    100  ~ 0
Park Laser
Text Notes 1850 4700 0    50   ~ 0
12V
Text Notes 4550 4200 0    50   ~ 0
12V
$Comp
L photo_detector_module:Photo_Detector_Module X1
U 1 1 61517D59
P 2700 2150
F 0 "X1" V 3050 2450 50  0000 L CNN
F 1 "Photo Detector Module" V 3150 1700 50  0000 L CNN
F 2 "" H 2800 2100 50  0001 C CNN
F 3 "" H 2800 2100 50  0001 C CNN
	1    2700 2150
	0    1    -1   0   
$EndComp
$Comp
L Device:R R19
U 1 1 61529B53
P 2950 3300
F 0 "R19" V 3050 3200 50  0000 C CNN
F 1 "1K" V 2850 3300 50  0000 C CNN
F 2 "" V 2880 3300 50  0001 C CNN
F 3 "~" H 2950 3300 50  0001 C CNN
	1    2950 3300
	0    1    1    0   
$EndComp
$Comp
L Device:R R20
U 1 1 6152B50B
P 3200 2950
F 0 "R20" V 3150 3150 50  0000 C CNN
F 1 "1K" V 3300 2950 50  0000 C CNN
F 2 "" V 3130 2950 50  0001 C CNN
F 3 "~" H 3200 2950 50  0001 C CNN
	1    3200 2950
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R21
U 1 1 6152C69B
P 3600 4150
F 0 "R21" H 3500 4250 50  0000 C CNN
F 1 "100" H 3450 4100 50  0000 C CNN
F 2 "" V 3530 4150 50  0001 C CNN
F 3 "~" H 3600 4150 50  0001 C CNN
	1    3600 4150
	1    0    0    1   
$EndComp
$Comp
L Isolator:4N25 U10
U 1 1 6152D3BB
P 3200 4750
F 0 "U10" H 3200 4550 50  0000 C CNN
F 1 "4N25" H 3200 4950 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 3000 4550 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 3200 4750 50  0001 L CNN
	1    3200 4750
	-1   0    0    -1  
$EndComp
Wire Wire Line
	2250 4850 2250 4950
Connection ~ 2650 3850
Wire Wire Line
	2550 2650 2550 2950
Wire Wire Line
	3350 2950 3400 2950
Wire Wire Line
	3400 2950 3400 3100
Wire Wire Line
	3400 3500 3400 3600
Wire Wire Line
	2650 3850 2650 4450
Wire Wire Line
	3600 4650 3500 4650
Wire Wire Line
	3500 4850 3600 4850
Wire Wire Line
	2350 4450 2650 4450
Wire Wire Line
	2350 4450 2350 4950
Wire Wire Line
	2250 4850 2900 4850
Wire Wire Line
	2150 4950 2150 4750
Wire Wire Line
	2150 4750 2900 4750
$Comp
L power:GND #PWR0136
U 1 1 615546D2
P 2650 4450
F 0 "#PWR0136" H 2650 4200 50  0001 C CNN
F 1 "GND" H 2655 4277 50  0000 C CNN
F 2 "" H 2650 4450 50  0001 C CNN
F 3 "" H 2650 4450 50  0001 C CNN
	1    2650 4450
	1    0    0    -1  
$EndComp
Connection ~ 2650 4450
$Comp
L power:GND #PWR0137
U 1 1 61554EE5
P 3400 3600
F 0 "#PWR0137" H 3400 3350 50  0001 C CNN
F 1 "GND" H 3405 3427 50  0000 C CNN
F 2 "" H 3400 3600 50  0001 C CNN
F 3 "" H 3400 3600 50  0001 C CNN
	1    3400 3600
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0138
U 1 1 6155571F
P 3600 4850
F 0 "#PWR0138" H 3600 4600 50  0001 C CNN
F 1 "GND" H 3605 4677 50  0000 C CNN
F 2 "" H 3600 4850 50  0001 C CNN
F 3 "" H 3600 4850 50  0001 C CNN
	1    3600 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2650 2650 2650 3850
Wire Wire Line
	3600 4300 3600 4650
$Comp
L Transistor_BJT:2N2219 Q1
U 1 1 61528C60
P 3300 3300
F 0 "Q1" H 3150 3450 50  0000 L CNN
F 1 "2N2222" H 3050 3150 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-39-3" H 3500 3225 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 3300 3300 50  0001 L CNN
	1    3300 3300
	1    0    0    -1  
$EndComp
NoConn ~ 2900 4650
Wire Wire Line
	2050 4500 2050 4950
Connection ~ 3400 2950
Wire Wire Line
	3400 2950 3600 2950
Wire Wire Line
	3600 4000 3600 2950
Wire Wire Line
	2750 3300 2800 3300
Wire Wire Line
	2750 2650 2750 3300
Wire Wire Line
	2050 2950 2550 2950
Connection ~ 2550 2950
Wire Wire Line
	3050 2950 2550 2950
Wire Wire Line
	2050 2950 2050 3850
Text Notes 3000 3600 0    50   ~ 0
(inverter)
$Comp
L Connector:RJ25 J?
U 1 1 61575782
P 7450 5350
AR Path="/6147F00D/61575782" Ref="J?"  Part="1" 
AR Path="/61524F60/61575782" Ref="J18"  Part="1" 
F 0 "J18" V 7550 4950 50  0000 C CNN
F 1 "RJ25" V 7450 4900 50  0000 C CNN
F 2 "" V 7450 5375 50  0001 C CNN
F 3 "~" V 7450 5375 50  0001 C CNN
	1    7450 5350
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7450 4950 7450 3700
Text Notes 7250 4900 1    50   ~ 0
Yellow
Text Notes 7350 4900 1    50   ~ 0
Green
Text Notes 7450 4900 1    50   ~ 0
Red
Text Notes 7550 4900 1    50   ~ 0
Black
NoConn ~ 7150 4950
NoConn ~ 7650 4950
Wire Wire Line
	7550 3450 7650 3450
Wire Wire Line
	7250 3350 7650 3350
Wire Wire Line
	7450 3700 7650 3700
Wire Wire Line
	7350 3600 7650 3600
Wire Wire Line
	7350 3600 7350 4950
Wire Wire Line
	7550 3450 7550 4950
Wire Wire Line
	7250 3350 7250 4950
Wire Notes Line
	6650 3050 6650 5750
Wire Notes Line
	6650 5750 8600 5750
Wire Notes Line
	8600 5750 8600 3050
Wire Notes Line
	6650 3050 8600 3050
Text Notes 7100 2950 0    100  ~ 0
FOB Module
Text Notes 5050 3700 0    50   ~ 0
381Ω\n(meas)
$Comp
L Device:Jumper_NC_Small JP1
U 1 1 615F8238
P 4750 2950
F 0 "JP1" V 4796 2902 50  0000 R CNN
F 1 "Disconnect" V 4705 2902 50  0000 R CNN
F 2 "" H 4750 2950 50  0001 C CNN
F 3 "~" H 4750 2950 50  0001 C CNN
	1    4750 2950
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4750 3050 4750 3450
Wire Wire Line
	4750 2300 4750 2850
Text Notes 1700 6000 0    50   ~ 0
NOTE: Park Laser and Detector are wired alike and should\nconnect to the “Park” port through an RJ11 splitter
Text Notes 6700 5900 0    50   ~ 0
Tigger wiring may be reverved; need to verify on install
$Comp
L Device:R_Variable_US VR23
U 1 1 615F052A
P 5200 3450
F 0 "VR23" V 4950 3450 50  0000 C CNN
F 1 "5K" V 5050 3450 50  0000 C CNN
F 2 "" V 5130 3450 50  0001 C CNN
F 3 "~" H 5200 3450 50  0001 C CNN
	1    5200 3450
	0    1    1    0   
$EndComp
$Comp
L Device:FOB X?
U 1 1 61575788
P 7900 3550
AR Path="/6147F00D/61575788" Ref="X?"  Part="1" 
AR Path="/61524F60/61575788" Ref="X2"  Part="1" 
F 0 "X2" H 8000 3200 50  0000 L CNN
F 1 "FOB" H 8200 3600 50  0000 L CNN
F 2 "" H 7950 3650 50  0001 C CNN
F 3 "" H 7950 3650 50  0001 C CNN
	1    7900 3550
	1    0    0    -1  
$EndComp
$EndSCHEMATC
