EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 3
Title "T-Rax Control Board"
Date "2021-05-06"
Rev "v1.6"
Comp "Robert Ferguson Observatory"
Comment1 "David Kensiski"
Comment2 "v1.4 add park sensor isolator (never implemented)"
Comment3 "v1.5 remove park isolator (see detector module); replace fob relay with isolator"
Comment4 "v1.6 merge all schematics into one doc; add accessory modules"
$EndDescr
$Comp
L Isolator:4N25 U1
U 1 1 608BB55B
P 5800 1450
F 0 "U1" H 5650 1650 50  0000 C CNN
F 1 "4N25" H 5900 1650 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5600 1250 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5800 1450 50  0001 L CNN
	1    5800 1450
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U2
U 1 1 608BE6B7
P 5800 2000
F 0 "U2" H 5650 2200 50  0000 C CNN
F 1 "4N25" H 5900 2200 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5600 1800 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5800 2000 50  0001 L CNN
	1    5800 2000
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U3
U 1 1 608C046E
P 5800 2500
F 0 "U3" H 5650 2700 50  0000 C CNN
F 1 "4N25" H 5900 2700 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5600 2300 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5800 2500 50  0001 L CNN
	1    5800 2500
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U4
U 1 1 608CB19D
P 5800 3000
F 0 "U4" H 5650 3200 50  0000 C CNN
F 1 "4N25" H 5900 3200 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5600 2800 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5800 3000 50  0001 L CNN
	1    5800 3000
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U5
U 1 1 608D438D
P 5800 3550
F 0 "U5" H 5650 3750 50  0000 C CNN
F 1 "4N25" H 5900 3750 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5600 3350 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5800 3550 50  0001 L CNN
	1    5800 3550
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U6
U 1 1 608D5F1A
P 5800 4050
F 0 "U6" H 5650 4250 50  0000 C CNN
F 1 "4N25" H 5900 4250 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5600 3850 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5800 4050 50  0001 L CNN
	1    5800 4050
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U7
U 1 1 608D96DF
P 5800 4750
F 0 "U7" H 5650 4950 50  0000 C CNN
F 1 "4N25" H 5900 4950 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5600 4550 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5800 4750 50  0001 L CNN
	1    5800 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 3100 7700 3100
Wire Wire Line
	6100 2600 6450 2600
Wire Wire Line
	6450 2950 7700 2950
Wire Wire Line
	6100 2100 6550 2100
Wire Wire Line
	6550 2800 7700 2800
$Comp
L power:+3.3V #PWR0101
U 1 1 6090D36A
P 6250 1450
F 0 "#PWR0101" H 6250 1300 50  0001 C CNN
F 1 "+3.3V" H 6265 1623 50  0000 C CNN
F 2 "" H 6250 1450 50  0001 C CNN
F 3 "" H 6250 1450 50  0001 C CNN
	1    6250 1450
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0102
U 1 1 6090F008
P 6250 2000
F 0 "#PWR0102" H 6250 1850 50  0001 C CNN
F 1 "+3.3V" H 6265 2173 50  0000 C CNN
F 2 "" H 6250 2000 50  0001 C CNN
F 3 "" H 6250 2000 50  0001 C CNN
	1    6250 2000
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0103
U 1 1 6090F405
P 6250 2500
F 0 "#PWR0103" H 6250 2350 50  0001 C CNN
F 1 "+3.3V" H 6300 2700 50  0000 C CNN
F 2 "" H 6250 2500 50  0001 C CNN
F 3 "" H 6250 2500 50  0001 C CNN
	1    6250 2500
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0104
U 1 1 6090F8A3
P 6250 3000
F 0 "#PWR0104" H 6250 2850 50  0001 C CNN
F 1 "+3.3V" H 6265 3173 50  0000 C CNN
F 2 "" H 6250 3000 50  0001 C CNN
F 3 "" H 6250 3000 50  0001 C CNN
	1    6250 3000
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0105
U 1 1 609101B9
P 6250 4050
F 0 "#PWR0105" H 6250 3900 50  0001 C CNN
F 1 "+3.3V" H 6265 4223 50  0000 C CNN
F 2 "" H 6250 4050 50  0001 C CNN
F 3 "" H 6250 4050 50  0001 C CNN
	1    6250 4050
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0106
U 1 1 609105FE
P 6250 4750
F 0 "#PWR0106" H 6250 4600 50  0001 C CNN
F 1 "+3.3V" H 6265 4923 50  0000 C CNN
F 2 "" H 6250 4750 50  0001 C CNN
F 3 "" H 6250 4750 50  0001 C CNN
	1    6250 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 3650 6450 3650
Wire Wire Line
	6450 3250 7700 3250
Wire Wire Line
	6100 4150 6550 4150
Wire Wire Line
	6550 3400 7700 3400
Wire Wire Line
	6650 3550 7700 3550
Wire Wire Line
	6650 2650 7700 2650
Wire Wire Line
	6650 1550 6100 1550
NoConn ~ 6100 1350
NoConn ~ 6100 1900
NoConn ~ 6100 2400
NoConn ~ 6100 2900
NoConn ~ 6100 3450
NoConn ~ 6100 3950
NoConn ~ 6100 4650
$Comp
L Connector:Conn_01x08_Male J1
U 1 1 6091DBEB
P 1800 1650
F 0 "J1" H 1908 2131 50  0000 C CNN
F 1 "Inputs" H 1908 2040 50  0000 C CNN
F 2 "Connector_JST:JST_XH_B8B-XH-A_1x08_P2.50mm_Vertical" H 1800 1650 50  0001 C CNN
F 3 "~" H 1800 1650 50  0001 C CNN
	1    1800 1650
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x06_Male J3
U 1 1 6091EF56
P 1800 5500
F 0 "J3" H 1908 5881 50  0000 C CNN
F 1 "Outputs" H 1908 5790 50  0000 C CNN
F 2 "Connector_JST:JST_XH_B6B-XH-A_1x06_P2.50mm_Vertical" H 1800 5500 50  0001 C CNN
F 3 "~" H 1800 5500 50  0001 C CNN
	1    1800 5500
	1    0    0    -1  
$EndComp
$Comp
L TRax-Controller-rescue:Raspberry_Pi_TRax-myLib-TRax-RaspberryPi-rescue-TRax-Controller-rescue J6
U 1 1 6089B0A9
P 8500 3500
F 0 "J6" H 9250 4900 50  0000 C CNN
F 1 "Raspberry Pi Header" H 9300 4800 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical" H 8500 3500 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 8500 3500 50  0001 C CNN
	1    8500 3500
	1    0    0    -1  
$EndComp
NoConn ~ 9300 2600
NoConn ~ 9300 2700
NoConn ~ 9300 2900
NoConn ~ 9300 3000
NoConn ~ 9300 3300
NoConn ~ 9300 3400
NoConn ~ 9300 3500
NoConn ~ 9300 3600
NoConn ~ 9300 3700
NoConn ~ 9300 3800
NoConn ~ 9300 4050
NoConn ~ 9300 4150
NoConn ~ 9300 4250
NoConn ~ 9300 4350
$Comp
L power:+3.3V #PWR0107
U 1 1 60939A05
P 8800 2000
F 0 "#PWR0107" H 8800 1850 50  0001 C CNN
F 1 "+3.3V" H 8815 2173 50  0000 C CNN
F 2 "" H 8800 2000 50  0001 C CNN
F 3 "" H 8800 2000 50  0001 C CNN
	1    8800 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	8800 2000 8800 2100
Wire Wire Line
	8700 2200 8700 2100
Wire Wire Line
	8700 2100 8800 2100
Connection ~ 8800 2100
Wire Wire Line
	8800 2100 8800 2200
$Comp
L power:GND #PWR0108
U 1 1 6093E379
P 8800 5000
F 0 "#PWR0108" H 8800 4750 50  0001 C CNN
F 1 "GND" H 8805 4827 50  0000 C CNN
F 2 "" H 8800 5000 50  0001 C CNN
F 3 "" H 8800 5000 50  0001 C CNN
	1    8800 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	8800 4800 8800 4900
Wire Wire Line
	8700 4800 8700 4900
Wire Wire Line
	8700 4900 8800 4900
Connection ~ 8800 4900
Wire Wire Line
	8800 4900 8800 5000
Wire Wire Line
	8600 4800 8600 4900
Wire Wire Line
	8600 4900 8700 4900
Connection ~ 8700 4900
Wire Wire Line
	8500 4800 8500 4900
Wire Wire Line
	8500 4900 8600 4900
Connection ~ 8600 4900
Wire Wire Line
	8400 4800 8400 4900
Wire Wire Line
	8400 4900 8500 4900
Connection ~ 8500 4900
Wire Wire Line
	8300 4800 8300 4900
Wire Wire Line
	8300 4900 8400 4900
Connection ~ 8400 4900
Wire Wire Line
	8200 4800 8200 4900
Wire Wire Line
	8200 4900 8300 4900
Connection ~ 8300 4900
Wire Wire Line
	8100 4800 8100 4900
Wire Wire Line
	8100 4900 8200 4900
Connection ~ 8200 4900
$Comp
L Connector:Conn_01x04_Male J5
U 1 1 6094BD83
P 7350 1050
F 0 "J5" V 7200 1000 50  0000 C CNN
F 1 "Grove LCD" V 7300 1000 50  0000 C CNN
F 2 "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical" H 7350 1050 50  0001 C CNN
F 3 "~" H 7350 1050 50  0001 C CNN
	1    7350 1050
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0110
U 1 1 6096403A
P 7450 1550
F 0 "#PWR0110" H 7450 1300 50  0001 C CNN
F 1 "GND" H 7455 1377 50  0000 C CNN
F 2 "" H 7450 1550 50  0001 C CNN
F 3 "" H 7450 1550 50  0001 C CNN
	1    7450 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	7250 2400 7700 2400
Wire Wire Line
	7150 2500 7700 2500
$Comp
L Device:R R8
U 1 1 6096D737
P 5100 1350
F 0 "R8" V 5000 1250 50  0000 C CNN
F 1 "1K" V 5000 1450 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 1350 50  0001 C CNN
F 3 "~" H 5100 1350 50  0001 C CNN
	1    5100 1350
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 1350 5250 1350
Wire Wire Line
	5500 1550 5350 1550
$Comp
L Device:C_Small C1
U 1 1 60995D07
P 4550 1450
F 0 "C1" H 4300 1500 50  0000 L CNN
F 1 "1000" H 4250 1400 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 4550 1450 50  0001 C CNN
F 3 "~" H 4550 1450 50  0001 C CNN
	1    4550 1450
	1    0    0    -1  
$EndComp
Connection ~ 4550 1350
$Comp
L power:GND #PWR0111
U 1 1 6099B3BD
P 4550 1550
F 0 "#PWR0111" H 4550 1300 50  0001 C CNN
F 1 "GND" H 4555 1377 50  0001 C CNN
F 2 "" H 4550 1550 50  0001 C CNN
F 3 "" H 4550 1550 50  0001 C CNN
	1    4550 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 1350 4700 1350
$Comp
L Device:R R9
U 1 1 609B6E35
P 5100 1900
F 0 "R9" V 5000 1800 50  0000 C CNN
F 1 "1K" V 5000 2000 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 1900 50  0001 C CNN
F 3 "~" H 5100 1900 50  0001 C CNN
	1    5100 1900
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 1900 5250 1900
Wire Wire Line
	5500 2100 5350 2100
$Comp
L Device:C_Small C2
U 1 1 609B6E43
P 4550 2000
F 0 "C2" H 4300 2050 50  0000 L CNN
F 1 "1000" H 4250 1950 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 4550 2000 50  0001 C CNN
F 3 "~" H 4550 2000 50  0001 C CNN
	1    4550 2000
	1    0    0    -1  
$EndComp
Connection ~ 4550 1900
$Comp
L power:GND #PWR0112
U 1 1 609B6E4A
P 4550 2100
F 0 "#PWR0112" H 4550 1850 50  0001 C CNN
F 1 "GND" H 4555 1927 50  0001 C CNN
F 2 "" H 4550 2100 50  0001 C CNN
F 3 "" H 4550 2100 50  0001 C CNN
	1    4550 2100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 1900 4700 1900
$Comp
L Device:R R10
U 1 1 609BA2CF
P 5100 2400
F 0 "R10" V 5000 2300 50  0000 C CNN
F 1 "1K" V 5000 2500 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 2400 50  0001 C CNN
F 3 "~" H 5100 2400 50  0001 C CNN
	1    5100 2400
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 2400 5250 2400
$Comp
L Device:C_Small C3
U 1 1 609BA2DD
P 4550 2500
F 0 "C3" H 4300 2550 50  0000 L CNN
F 1 "1000" H 4250 2450 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 4550 2500 50  0001 C CNN
F 3 "~" H 4550 2500 50  0001 C CNN
	1    4550 2500
	1    0    0    -1  
$EndComp
Connection ~ 4550 2400
$Comp
L power:GND #PWR0113
U 1 1 609BA2E4
P 4550 2600
F 0 "#PWR0113" H 4550 2350 50  0001 C CNN
F 1 "GND" H 4555 2427 50  0001 C CNN
F 2 "" H 4550 2600 50  0001 C CNN
F 3 "" H 4550 2600 50  0001 C CNN
	1    4550 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 2400 4700 2400
$Comp
L Device:R R11
U 1 1 609BD628
P 5100 2900
F 0 "R11" V 5000 2800 50  0000 C CNN
F 1 "1K" V 5000 3000 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 2900 50  0001 C CNN
F 3 "~" H 5100 2900 50  0001 C CNN
	1    5100 2900
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 2900 5250 2900
Wire Wire Line
	5500 3100 5350 3100
$Comp
L Device:C_Small C4
U 1 1 609BD636
P 4550 3000
F 0 "C4" H 4300 3050 50  0000 L CNN
F 1 "1000" H 4250 2950 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 4550 3000 50  0001 C CNN
F 3 "~" H 4550 3000 50  0001 C CNN
	1    4550 3000
	1    0    0    -1  
$EndComp
Connection ~ 4550 2900
$Comp
L power:GND #PWR0114
U 1 1 609BD63D
P 4550 3100
F 0 "#PWR0114" H 4550 2850 50  0001 C CNN
F 1 "GND" H 4555 2927 50  0001 C CNN
F 2 "" H 4550 3100 50  0001 C CNN
F 3 "" H 4550 3100 50  0001 C CNN
	1    4550 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 2900 4700 2900
$Comp
L Device:R R12
U 1 1 609C2209
P 5100 3450
F 0 "R12" V 5000 3350 50  0000 C CNN
F 1 "1K" V 5000 3550 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 3450 50  0001 C CNN
F 3 "~" H 5100 3450 50  0001 C CNN
	1    5100 3450
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 3650 5350 3650
$Comp
L Device:C_Small C5
U 1 1 609C2217
P 4550 3550
F 0 "C5" H 4300 3600 50  0000 L CNN
F 1 "1000" H 4250 3500 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 4550 3550 50  0001 C CNN
F 3 "~" H 4550 3550 50  0001 C CNN
	1    4550 3550
	1    0    0    -1  
$EndComp
Connection ~ 4550 3450
$Comp
L power:GND #PWR0115
U 1 1 609C221E
P 4550 3650
F 0 "#PWR0115" H 4550 3400 50  0001 C CNN
F 1 "GND" H 4555 3477 50  0001 C CNN
F 2 "" H 4550 3650 50  0001 C CNN
F 3 "" H 4550 3650 50  0001 C CNN
	1    4550 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 3450 4700 3450
$Comp
L Device:R R13
U 1 1 609C6E88
P 5100 3950
F 0 "R13" V 5000 3850 50  0000 C CNN
F 1 "1K" V 5000 4050 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 3950 50  0001 C CNN
F 3 "~" H 5100 3950 50  0001 C CNN
	1    5100 3950
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 4150 5350 4150
$Comp
L Device:C_Small C6
U 1 1 609C6E96
P 4550 4050
F 0 "C6" H 4300 4100 50  0000 L CNN
F 1 "1000" H 4250 4000 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 4550 4050 50  0001 C CNN
F 3 "~" H 4550 4050 50  0001 C CNN
	1    4550 4050
	1    0    0    -1  
$EndComp
Connection ~ 4550 3950
$Comp
L power:GND #PWR0116
U 1 1 609C6E9D
P 4550 4150
F 0 "#PWR0116" H 4550 3900 50  0001 C CNN
F 1 "GND" H 4555 3977 50  0001 C CNN
F 2 "" H 4550 4150 50  0001 C CNN
F 3 "" H 4550 4150 50  0001 C CNN
	1    4550 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 3950 4700 3950
$Comp
L Device:R R14
U 1 1 609CC195
P 5100 4650
F 0 "R14" V 5000 4550 50  0000 C CNN
F 1 "1K" V 5000 4750 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 4650 50  0001 C CNN
F 3 "~" H 5100 4650 50  0001 C CNN
	1    5100 4650
	0    1    1    0   
$EndComp
$Comp
L Device:C_Small C7
U 1 1 609CC1A3
P 4550 4750
F 0 "C7" H 4300 4800 50  0000 L CNN
F 1 "1000" H 4250 4700 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 4550 4750 50  0001 C CNN
F 3 "~" H 4550 4750 50  0001 C CNN
	1    4550 4750
	1    0    0    -1  
$EndComp
Connection ~ 4550 4650
Wire Wire Line
	4550 4650 4700 4650
$Comp
L power:GND #PWR0117
U 1 1 609ECAFE
P 5350 1550
F 0 "#PWR0117" H 5350 1300 50  0001 C CNN
F 1 "GND" H 5355 1377 50  0001 C CNN
F 2 "" H 5350 1550 50  0001 C CNN
F 3 "" H 5350 1550 50  0001 C CNN
	1    5350 1550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0118
U 1 1 609ED729
P 5350 2100
F 0 "#PWR0118" H 5350 1850 50  0001 C CNN
F 1 "GND" H 5355 1927 50  0001 C CNN
F 2 "" H 5350 2100 50  0001 C CNN
F 3 "" H 5350 2100 50  0001 C CNN
	1    5350 2100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0119
U 1 1 609EDFCB
P 5350 2600
F 0 "#PWR0119" H 5350 2350 50  0001 C CNN
F 1 "GND" H 5355 2427 50  0001 C CNN
F 2 "" H 5350 2600 50  0001 C CNN
F 3 "" H 5350 2600 50  0001 C CNN
	1    5350 2600
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0120
U 1 1 609EEA7B
P 5350 3100
F 0 "#PWR0120" H 5350 2850 50  0001 C CNN
F 1 "GND" H 5450 3000 50  0001 C CNN
F 2 "" H 5350 3100 50  0001 C CNN
F 3 "" H 5350 3100 50  0001 C CNN
	1    5350 3100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0121
U 1 1 609EF16D
P 5350 3650
F 0 "#PWR0121" H 5350 3400 50  0001 C CNN
F 1 "GND" H 5450 3550 50  0001 C CNN
F 2 "" H 5350 3650 50  0001 C CNN
F 3 "" H 5350 3650 50  0001 C CNN
	1    5350 3650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0122
U 1 1 609EF86B
P 5350 4150
F 0 "#PWR0122" H 5350 3900 50  0001 C CNN
F 1 "GND" H 5450 4050 50  0001 C CNN
F 2 "" H 5350 4150 50  0001 C CNN
F 3 "" H 5350 4150 50  0001 C CNN
	1    5350 4150
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0123
U 1 1 6090FCBF
P 6250 3550
F 0 "#PWR0123" H 6250 3400 50  0001 C CNN
F 1 "+3.3V" H 6265 3723 50  0000 C CNN
F 2 "" H 6250 3550 50  0001 C CNN
F 3 "" H 6250 3550 50  0001 C CNN
	1    6250 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 4750 6250 4750
Wire Wire Line
	6100 4050 6250 4050
Wire Wire Line
	6100 3550 6250 3550
Wire Wire Line
	6100 3000 6250 3000
Wire Wire Line
	6100 2000 6250 2000
Wire Wire Line
	6100 1450 6250 1450
Wire Wire Line
	6100 4850 6650 4850
Wire Wire Line
	2000 1350 4550 1350
Wire Wire Line
	4050 1900 4550 1900
Wire Wire Line
	2000 1450 4050 1450
Wire Wire Line
	3950 2400 4550 2400
Wire Wire Line
	2000 1550 3950 1550
Wire Wire Line
	2000 1650 3850 1650
Wire Wire Line
	3850 2900 4550 2900
Wire Wire Line
	2000 1750 3750 1750
Wire Wire Line
	3750 3450 4550 3450
Wire Wire Line
	2000 1850 3650 1850
Wire Wire Line
	3650 3950 4550 3950
$Comp
L power:GND #PWR0124
U 1 1 60A449B5
P 2200 2150
F 0 "#PWR0124" H 2200 1900 50  0001 C CNN
F 1 "GND" H 2205 1977 50  0000 C CNN
F 2 "" H 2200 2150 50  0001 C CNN
F 3 "" H 2200 2150 50  0001 C CNN
	1    2200 2150
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0125
U 1 1 60A454E6
P 2700 1950
F 0 "#PWR0125" H 2700 1800 50  0001 C CNN
F 1 "+3.3V" V 2715 2078 50  0000 L CNN
F 2 "" H 2700 1950 50  0001 C CNN
F 3 "" H 2700 1950 50  0001 C CNN
	1    2700 1950
	0    1    1    0   
$EndComp
Wire Wire Line
	2200 2050 2200 2150
Wire Wire Line
	2000 2050 2200 2050
$Comp
L power:GND #PWR0126
U 1 1 60A63C63
P 2400 5900
F 0 "#PWR0126" H 2400 5650 50  0001 C CNN
F 1 "GND" H 2405 5727 50  0000 C CNN
F 2 "" H 2400 5900 50  0001 C CNN
F 3 "" H 2400 5900 50  0001 C CNN
	1    2400 5900
	1    0    0    -1  
$EndComp
Wire Wire Line
	2400 5800 2400 5900
Wire Wire Line
	2000 5800 2400 5800
Wire Wire Line
	2000 5600 7300 5600
Wire Wire Line
	2000 5500 7200 5500
Wire Wire Line
	2000 5400 7100 5400
Wire Wire Line
	2000 5300 7000 5300
Wire Wire Line
	7000 5300 7000 3800
Wire Wire Line
	7000 3800 7700 3800
Wire Wire Line
	7100 5400 7100 3950
Wire Wire Line
	7100 3950 7700 3950
Wire Wire Line
	7200 4100 7200 5500
Wire Wire Line
	7200 4100 7700 4100
Wire Wire Line
	7300 5600 7300 4250
Wire Wire Line
	7300 4250 7700 4250
$Comp
L Device:R R15
U 1 1 60B6898E
P 7550 5650
F 0 "R15" H 7620 5696 50  0000 L CNN
F 1 "330" H 7620 5605 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 7480 5650 50  0001 C CNN
F 3 "~" H 7550 5650 50  0001 C CNN
	1    7550 5650
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 60B6AB99
P 7550 6050
F 0 "D1" V 7589 5932 50  0000 R CNN
F 1 "Green" V 7498 5932 50  0000 R CNN
F 2 "LED_THT:LED_D5.0mm" H 7550 6050 50  0001 C CNN
F 3 "~" H 7550 6050 50  0001 C CNN
	1    7550 6050
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0127
U 1 1 60B6CDBB
P 7550 6300
F 0 "#PWR0127" H 7550 6050 50  0001 C CNN
F 1 "GND" H 7555 6127 50  0000 C CNN
F 2 "" H 7550 6300 50  0001 C CNN
F 3 "" H 7550 6300 50  0001 C CNN
	1    7550 6300
	1    0    0    -1  
$EndComp
Wire Wire Line
	7700 4400 7550 4400
Wire Wire Line
	7550 5800 7550 5900
Wire Wire Line
	7550 6200 7550 6300
$Comp
L Connector:Conn_01x02_Male J2
U 1 1 60BB16A3
P 1800 4650
F 0 "J2" H 1908 4831 50  0000 C CNN
F 1 "BldgPwr" H 1908 4740 50  0000 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 1800 4650 50  0001 C CNN
F 3 "~" H 1800 4650 50  0001 C CNN
	1    1800 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 4650 4550 4650
Wire Wire Line
	4000 4750 2000 4750
Wire Wire Line
	7150 1250 7150 2500
Wire Wire Line
	7250 1250 7250 2400
Wire Wire Line
	7450 1250 7450 1550
Wire Wire Line
	6650 3550 6650 4850
Wire Wire Line
	6550 3400 6550 4150
Wire Wire Line
	6450 3250 6450 3650
Wire Wire Line
	6450 2600 6450 2950
Wire Wire Line
	6550 2100 6550 2800
Wire Wire Line
	6650 1550 6650 2650
Wire Wire Line
	4050 1450 4050 1900
Wire Wire Line
	3950 1550 3950 2400
Wire Wire Line
	3850 1650 3850 2900
Wire Wire Line
	3750 1750 3750 3450
Wire Wire Line
	3650 1850 3650 3950
$Comp
L Device:R R16
U 1 1 60D001D7
P 8050 5650
F 0 "R16" H 8120 5696 50  0000 L CNN
F 1 "330" H 8120 5605 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 7980 5650 50  0001 C CNN
F 3 "~" H 8050 5650 50  0001 C CNN
	1    8050 5650
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D2
U 1 1 60D001DD
P 8050 6050
F 0 "D2" V 8089 5932 50  0000 R CNN
F 1 "Red" V 7998 5932 50  0000 R CNN
F 2 "LED_THT:LED_D5.0mm" H 8050 6050 50  0001 C CNN
F 3 "~" H 8050 6050 50  0001 C CNN
	1    8050 6050
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0128
U 1 1 60D001E3
P 8050 6300
F 0 "#PWR0128" H 8050 6050 50  0001 C CNN
F 1 "GND" H 8055 6127 50  0000 C CNN
F 2 "" H 8050 6300 50  0001 C CNN
F 3 "" H 8050 6300 50  0001 C CNN
	1    8050 6300
	1    0    0    -1  
$EndComp
Wire Wire Line
	8050 5800 8050 5900
Wire Wire Line
	8050 6200 8050 6300
Wire Wire Line
	7550 4400 7550 5500
$Comp
L power:+3.3V #PWR0129
U 1 1 60D24F40
P 8050 5500
F 0 "#PWR0129" H 8050 5350 50  0001 C CNN
F 1 "+3.3V" H 8065 5673 50  0000 C CNN
F 2 "" H 8050 5500 50  0001 C CNN
F 3 "" H 8050 5500 50  0001 C CNN
	1    8050 5500
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 5700 2700 5700
Text Notes 1750 4850 0    50   ~ 0
(Not UPS)
Text Notes 7150 1150 0    39   ~ 0
Y  W  R  B
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 608D0375
P 11550 7800
F 0 "#FLG0101" H 11550 7875 50  0001 C CNN
F 1 "PWR_FLAG" H 11550 7973 50  0000 C CNN
F 2 "" H 11550 7800 50  0001 C CNN
F 3 "~" H 11550 7800 50  0001 C CNN
	1    11550 7800
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 608D1C6B
P 11850 7800
F 0 "#FLG0102" H 11850 7875 50  0001 C CNN
F 1 "PWR_FLAG" H 11850 7973 50  0000 C CNN
F 2 "" H 11850 7800 50  0001 C CNN
F 3 "~" H 11850 7800 50  0001 C CNN
	1    11850 7800
	-1   0    0    1   
$EndComp
$Comp
L power:+3.3V #PWR0131
U 1 1 608D2B2B
P 11850 7800
F 0 "#PWR0131" H 11850 7650 50  0001 C CNN
F 1 "+3.3V" H 11865 7973 50  0000 C CNN
F 2 "" H 11850 7800 50  0001 C CNN
F 3 "" H 11850 7800 50  0001 C CNN
	1    11850 7800
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0132
U 1 1 608D3AD7
P 11550 7800
F 0 "#PWR0132" H 11550 7550 50  0001 C CNN
F 1 "GND" H 11555 7627 50  0000 C CNN
F 2 "" H 11550 7800 50  0001 C CNN
F 3 "" H 11550 7800 50  0001 C CNN
	1    11550 7800
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R1
U 1 1 60901392
P 4700 1450
F 0 "R1" H 4759 1496 50  0000 L CNN
F 1 "10K" H 4759 1405 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4700 1450 50  0001 C CNN
F 3 "~" H 4700 1450 50  0001 C CNN
	1    4700 1450
	1    0    0    -1  
$EndComp
Connection ~ 4700 1350
$Comp
L Device:R_Small R2
U 1 1 6090298E
P 4700 2000
F 0 "R2" H 4759 2046 50  0000 L CNN
F 1 "10K" H 4759 1955 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4700 2000 50  0001 C CNN
F 3 "~" H 4700 2000 50  0001 C CNN
	1    4700 2000
	1    0    0    -1  
$EndComp
Connection ~ 4700 1900
Connection ~ 4700 2400
$Comp
L Device:R_Small R3
U 1 1 609045CE
P 4700 2500
F 0 "R3" H 4759 2546 50  0000 L CNN
F 1 "10K" H 4759 2455 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4700 2500 50  0001 C CNN
F 3 "~" H 4700 2500 50  0001 C CNN
	1    4700 2500
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R4
U 1 1 60904E09
P 4700 3000
F 0 "R4" H 4759 3046 50  0000 L CNN
F 1 "10K" H 4759 2955 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4700 3000 50  0001 C CNN
F 3 "~" H 4700 3000 50  0001 C CNN
	1    4700 3000
	1    0    0    -1  
$EndComp
Connection ~ 4700 2900
$Comp
L Device:R_Small R5
U 1 1 6090593A
P 4700 3550
F 0 "R5" H 4759 3596 50  0000 L CNN
F 1 "10K" H 4759 3505 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4700 3550 50  0001 C CNN
F 3 "~" H 4700 3550 50  0001 C CNN
	1    4700 3550
	1    0    0    -1  
$EndComp
Connection ~ 4700 3450
$Comp
L Device:R_Small R6
U 1 1 60906300
P 4700 4050
F 0 "R6" H 4759 4096 50  0000 L CNN
F 1 "10K" H 4759 4005 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4700 4050 50  0001 C CNN
F 3 "~" H 4700 4050 50  0001 C CNN
	1    4700 4050
	1    0    0    -1  
$EndComp
Connection ~ 4700 3950
$Comp
L Device:R_Small R7
U 1 1 60906CA2
P 4700 4750
F 0 "R7" H 4759 4796 50  0000 L CNN
F 1 "10K" H 4759 4705 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4700 4750 50  0001 C CNN
F 3 "~" H 4700 4750 50  0001 C CNN
	1    4700 4750
	1    0    0    -1  
$EndComp
Connection ~ 4700 4650
Wire Wire Line
	5500 2600 5350 2600
Wire Wire Line
	4000 4850 4000 4750
Wire Wire Line
	4000 4850 4550 4850
Connection ~ 4550 4850
Wire Wire Line
	4550 4850 4700 4850
Connection ~ 4700 4850
Wire Wire Line
	4700 4850 5500 4850
$Comp
L power:GND #PWR01
U 1 1 60AEE47B
P 4700 1550
F 0 "#PWR01" H 4700 1300 50  0001 C CNN
F 1 "GND" H 4705 1377 50  0001 C CNN
F 2 "" H 4700 1550 50  0001 C CNN
F 3 "" H 4700 1550 50  0001 C CNN
	1    4700 1550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR02
U 1 1 60AEEC7A
P 4700 2100
F 0 "#PWR02" H 4700 1850 50  0001 C CNN
F 1 "GND" H 4705 1927 50  0001 C CNN
F 2 "" H 4700 2100 50  0001 C CNN
F 3 "" H 4700 2100 50  0001 C CNN
	1    4700 2100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR03
U 1 1 60AEF480
P 4700 2600
F 0 "#PWR03" H 4700 2350 50  0001 C CNN
F 1 "GND" H 4705 2427 50  0001 C CNN
F 2 "" H 4700 2600 50  0001 C CNN
F 3 "" H 4700 2600 50  0001 C CNN
	1    4700 2600
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 60AEFC92
P 4700 3100
F 0 "#PWR04" H 4700 2850 50  0001 C CNN
F 1 "GND" H 4705 2927 50  0001 C CNN
F 2 "" H 4700 3100 50  0001 C CNN
F 3 "" H 4700 3100 50  0001 C CNN
	1    4700 3100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR05
U 1 1 60AF0B4A
P 4700 3650
F 0 "#PWR05" H 4700 3400 50  0001 C CNN
F 1 "GND" H 4705 3477 50  0001 C CNN
F 2 "" H 4700 3650 50  0001 C CNN
F 3 "" H 4700 3650 50  0001 C CNN
	1    4700 3650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR06
U 1 1 60AF1374
P 4700 4150
F 0 "#PWR06" H 4700 3900 50  0001 C CNN
F 1 "GND" H 4705 3977 50  0001 C CNN
F 2 "" H 4700 4150 50  0001 C CNN
F 3 "" H 4700 4150 50  0001 C CNN
	1    4700 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5500 3450 5250 3450
Wire Wire Line
	5500 3950 5250 3950
Wire Wire Line
	5500 4650 5250 4650
Wire Wire Line
	4700 1350 4950 1350
Wire Wire Line
	4700 1900 4950 1900
Wire Wire Line
	4700 2400 4950 2400
Wire Wire Line
	4700 2900 4950 2900
Wire Wire Line
	4700 3450 4950 3450
Wire Wire Line
	4700 3950 4950 3950
Wire Wire Line
	4700 4650 4950 4650
Text Notes 1700 1900 1    50   ~ 0
From Inputs
Text Notes 1700 5700 1    50   ~ 0
To Relays
$Comp
L power:+3.3V #PWR0109
U 1 1 6096CA6A
P 2700 5700
F 0 "#PWR0109" H 2700 5550 50  0001 C CNN
F 1 "+3.3V" V 2715 5828 50  0000 L CNN
F 2 "" H 2700 5700 50  0001 C CNN
F 3 "" H 2700 5700 50  0001 C CNN
	1    2700 5700
	0    1    1    0   
$EndComp
Wire Wire Line
	6100 2500 6250 2500
Wire Wire Line
	8400 2200 8400 2100
Wire Wire Line
	8400 2100 8500 2100
Wire Wire Line
	8500 2100 8500 2200
Wire Wire Line
	8400 2100 7350 2100
Connection ~ 8400 2100
Wire Wire Line
	7350 1250 7350 2100
Wire Wire Line
	2000 1950 2700 1950
$Comp
L power:PWR_FLAG #FLG0103
U 1 1 60A1CC87
P 12150 7800
F 0 "#FLG0103" H 12150 7875 50  0001 C CNN
F 1 "PWR_FLAG" H 12150 7973 50  0000 C CNN
F 2 "" H 12150 7800 50  0001 C CNN
F 3 "~" H 12150 7800 50  0001 C CNN
	1    12150 7800
	1    0    0    1   
$EndComp
$Comp
L power:+5V #PWR0130
U 1 1 60A2A59E
P 12150 7800
F 0 "#PWR0130" H 12150 7650 50  0001 C CNN
F 1 "+5V" H 12165 7973 50  0000 C CNN
F 2 "" H 12150 7800 50  0001 C CNN
F 3 "" H 12150 7800 50  0001 C CNN
	1    12150 7800
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0133
U 1 1 60A2B722
P 8500 2000
F 0 "#PWR0133" H 8500 1850 50  0001 C CNN
F 1 "+5V" H 8515 2173 50  0000 C CNN
F 2 "" H 8500 2000 50  0001 C CNN
F 3 "" H 8500 2000 50  0001 C CNN
	1    8500 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	8500 2000 8500 2100
Connection ~ 8500 2100
$Sheet
S 11700 700  1150 400 
U 6146FF07
F0 "TRax Relays" 50
F1 "TRax-Relays.sch" 50
$EndSheet
$Sheet
S 11700 2250 1150 350 
U 61524F60
F0 "TRax Laser Park Detector" 50
F1 "TRax-LaserParkDetector.sch" 50
$EndSheet
$EndSCHEMATC
