EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 2 3
Title "T-Rax Relays & Connector wiring"
Date "2021-10-17"
Rev "v1.6"
Comp "Robert Ferguson Observatory"
Comment1 "David Kensiski"
Comment2 "v1.4 add park sensor isolator (never implemented)"
Comment3 "v1.5 remove park isolator (see detector module); replace fob relay with isolator"
Comment4 "v1.6 merge all schematics into one doc; add accessory modules"
$EndDescr
Text Notes 5450 1050 2    50   ~ 0
Violet
Text Notes 5450 1750 2    50   ~ 0
Black
Text Notes 5450 1650 2    50   ~ 0
Red
Text Notes 5450 1550 2    50   ~ 0
White
Text Notes 5450 1450 2    50   ~ 0
Yellow
Text Notes 5450 1350 2    50   ~ 0
Orange
Text Notes 5450 1250 2    50   ~ 0
Green
Text Notes 5450 1150 2    50   ~ 0
Blue
Entry Wire Line
	9000 2550 9100 2450
Entry Wire Line
	9200 2450 9100 2550
Entry Wire Line
	9300 2450 9200 2550
Entry Wire Line
	9000 2450 8900 2550
Entry Wire Line
	8900 2450 8800 2550
Entry Wire Line
	9400 2450 9300 2550
Text Notes 9300 2600 3    50   ~ 0
Black
Text Notes 9200 2600 3    50   ~ 0
Red
Text Notes 9100 2600 3    50   ~ 0
White
Text Notes 9000 2600 3    50   ~ 0
Yellow
Text Notes 8900 2600 3    50   ~ 0
Orange
Text Notes 8800 2600 3    50   ~ 0
Green
$Comp
L Connector:6P6C J8
U 1 1 609A2420
P 1600 3600
F 0 "J8" H 1200 3600 50  0000 C CNN
F 1 "MountPower" H 1657 4076 50  0000 C CNN
F 2 "" V 1600 3625 50  0001 C CNN
F 3 "~" V 1600 3625 50  0001 C CNN
	1    1600 3600
	1    0    0    -1  
$EndComp
$Comp
L Connector:6P6C J7
U 1 1 609A2BC1
P 1600 2600
F 0 "J7" H 1200 2600 50  0000 C CNN
F 1 "RoofPower" H 1657 3076 50  0000 C CNN
F 2 "" V 1600 2625 50  0001 C CNN
F 3 "~" V 1600 2625 50  0001 C CNN
	1    1600 2600
	1    0    0    -1  
$EndComp
$Comp
L Connector:6P6C J9
U 1 1 609A37E0
P 1600 4600
F 0 "J9" H 1200 4600 50  0000 C CNN
F 1 "Open/Close" H 1657 5076 50  0000 C CNN
F 2 "" V 1600 4625 50  0001 C CNN
F 3 "~" V 1600 4625 50  0001 C CNN
	1    1600 4600
	1    0    0    -1  
$EndComp
$Comp
L Connector:6P6C J10
U 1 1 609A462B
P 1600 5600
F 0 "J10" H 1200 5600 50  0000 C CNN
F 1 "Parked" H 1657 6076 50  0000 C CNN
F 2 "" V 1600 5625 50  0001 C CNN
F 3 "~" V 1600 5625 50  0001 C CNN
	1    1600 5600
	1    0    0    -1  
$EndComp
Text Notes 1050 7550 0    50   ~ 0
RJ Color Code: Telco (Cat5)\n5. Yellow (Orange/White)\n4. Green  (White/Blue)\n3. Red    (Blue/White)\n2. Black  (White/Orange
Wire Wire Line
	2000 1550 3150 1550
Wire Wire Line
	2000 2600 3250 2600
Wire Wire Line
	2000 3600 3350 3600
Wire Wire Line
	2000 4600 3450 4600
Wire Wire Line
	2000 4400 3550 4400
Text Notes 10500 2450 2    50   ~ 0
Outputs from\nControl Board
Text Notes 10500 1950 2    50   ~ 0
Inputs from\nControl Board
Wire Wire Line
	7800 2900 8100 2900
Wire Wire Line
	7800 3100 8200 3100
Wire Wire Line
	8100 2900 8100 3700
Wire Wire Line
	8100 5300 7800 5300
Connection ~ 8100 2900
Wire Wire Line
	8200 3100 8200 3900
Wire Wire Line
	8200 5500 7800 5500
Connection ~ 8200 3100
Wire Wire Line
	7800 3700 8100 3700
Connection ~ 8100 3700
Wire Wire Line
	7800 3900 8200 3900
Connection ~ 8200 3900
$Comp
L power:+12V #PWR0134
U 1 1 60A1C6F9
P 6350 6300
F 0 "#PWR0134" H 6350 6150 50  0001 C CNN
F 1 "+12V" H 6250 6350 50  0000 C CNN
F 2 "" H 6350 6300 50  0001 C CNN
F 3 "" H 6350 6300 50  0001 C CNN
	1    6350 6300
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0135
U 1 1 60A26175
P 6250 6300
F 0 "#PWR0135" H 6250 6050 50  0001 C CNN
F 1 "GND" H 6100 6250 50  0000 C CNN
F 2 "" H 6250 6300 50  0001 C CNN
F 3 "" H 6250 6300 50  0001 C CNN
	1    6250 6300
	1    0    0    -1  
$EndComp
NoConn ~ 6900 2900
NoConn ~ 6900 3700
NoConn ~ 6900 5300
NoConn ~ 2000 1650
NoConn ~ 2000 1350
Wire Wire Line
	6900 3800 6800 3800
Wire Wire Line
	2000 5400 4150 5400
$Comp
L Connector:6P6C J11
U 1 1 609A546C
P 1600 6600
F 0 "J11" H 1200 6600 50  0000 C CNN
F 1 "Fob" H 1657 7076 50  0000 C CNN
F 2 "" V 1600 6625 50  0001 C CNN
F 3 "~" V 1600 6625 50  0001 C CNN
	1    1600 6600
	1    0    0    -1  
$EndComp
Text Notes 3400 5400 2    50   ~ 0
12V switched
Wire Wire Line
	2000 2400 3950 2400
Wire Wire Line
	2000 3400 3950 3400
Wire Wire Line
	6800 3000 6900 3000
Connection ~ 6800 3800
Wire Wire Line
	6800 3800 6800 4500
Wire Wire Line
	2000 6500 4050 6500
$Comp
L Connector:Conn_01x07_Male J15
U 1 1 60B04D3A
P 5850 3300
F 0 "J15" H 5900 2800 50  0000 C CNN
F 1 "Relays" H 5950 2900 50  0000 C CNN
F 2 "" H 5850 3300 50  0001 C CNN
F 3 "~" H 5850 3300 50  0001 C CNN
	1    5850 3300
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x07_Male J13
U 1 1 60AFF249
P 5700 3300
F 0 "J13" H 5850 2800 50  0000 R CNN
F 1 "Relays" H 5950 2900 50  0000 R CNN
F 2 "" H 5700 3300 50  0001 C CNN
F 3 "~" H 5700 3300 50  0001 C CNN
	1    5700 3300
	-1   0    0    -1  
$EndComp
Connection ~ 6800 3000
Wire Wire Line
	6050 3100 6900 3100
Wire Wire Line
	6800 3000 6800 3800
Wire Wire Line
	6650 3200 6650 3900
Wire Wire Line
	6050 3200 6650 3200
Wire Wire Line
	6650 3900 6900 3900
Wire Wire Line
	6050 3300 6550 3300
Wire Wire Line
	3950 3100 3950 2400
Wire Wire Line
	3950 3200 3950 3400
Wire Wire Line
	4050 3300 4050 6500
Wire Wire Line
	3850 6600 3850 3700
Connection ~ 3850 3700
Wire Wire Line
	2000 6600 3850 6600
Wire Wire Line
	2000 3700 3850 3700
Wire Wire Line
	2000 2700 3850 2700
Wire Wire Line
	6050 3400 6450 3400
Wire Wire Line
	4150 3400 4150 5400
Wire Wire Line
	2000 6700 4350 6700
Wire Wire Line
	6050 3500 6350 3500
Wire Wire Line
	6050 3600 6250 3600
Wire Wire Line
	6250 3600 6250 6300
Wire Wire Line
	4350 3600 4350 5700
Connection ~ 4350 5700
Wire Wire Line
	4350 5700 4350 6700
Wire Wire Line
	2000 6400 4250 6400
Wire Wire Line
	4250 3500 4250 6400
Text Notes 3050 6400 2    50   ~ 0
12V\n
Wire Wire Line
	3850 2700 3850 3000
Connection ~ 3850 3000
Wire Wire Line
	3850 3000 3850 3700
Wire Notes Line
	5800 5750 5800 2350
Text Notes 6550 2500 2    79   ~ 0
Relay Board
$Comp
L Connector:Conn_01x08_Male J12
U 1 1 6105C513
P 5700 1350
F 0 "J12" H 5850 750 50  0000 R CNN
F 1 "Inputs" H 6000 850 50  0000 R CNN
F 2 "" H 5700 1350 50  0001 C CNN
F 3 "~" H 5700 1350 50  0001 C CNN
	1    5700 1350
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3550 1450 3550 4400
Wire Wire Line
	3450 1350 3450 4600
Wire Wire Line
	3350 1250 3350 3600
Wire Wire Line
	3250 1150 3250 2600
Wire Wire Line
	2000 1450 3050 1450
Wire Wire Line
	2000 2500 3050 2500
Connection ~ 3050 2500
Wire Wire Line
	3050 2500 3050 3500
Wire Wire Line
	2000 3500 3050 3500
Connection ~ 3050 3500
Wire Wire Line
	3050 3500 3050 4500
Wire Wire Line
	2000 4500 3050 4500
Connection ~ 3050 4500
Wire Wire Line
	3050 4500 3050 4700
Wire Wire Line
	2000 4700 3050 4700
Wire Notes Line
	2750 750  2750 7050
Wire Notes Line
	5750 750  5750 7050
Text Notes 3800 900  2    79   ~ 0
Connector Board
Entry Wire Line
	6200 1850 6100 1750
Entry Wire Line
	6200 1150 6100 1050
Entry Wire Line
	6200 1250 6100 1150
Entry Wire Line
	6200 1350 6100 1250
Entry Wire Line
	6200 1450 6100 1350
Entry Wire Line
	6200 1550 6100 1450
Entry Wire Line
	6200 1650 6100 1550
Entry Wire Line
	6200 1750 6100 1650
$Comp
L Connector_Generic:Conn_01x08 J14
U 1 1 611FE672
P 5850 1350
F 0 "J14" H 5850 750 50  0000 C CNN
F 1 "Inputs" H 5800 850 50  0000 C CNN
F 2 "" H 5850 1350 50  0001 C CNN
F 3 "~" H 5850 1350 50  0001 C CNN
	1    5850 1350
	-1   0    0    -1  
$EndComp
Wire Wire Line
	6050 1050 6100 1050
Wire Wire Line
	6050 1150 6100 1150
Wire Wire Line
	6050 1250 6100 1250
Wire Wire Line
	6050 1350 6100 1350
Wire Wire Line
	6050 1450 6100 1450
Wire Wire Line
	6050 1550 6100 1550
Wire Wire Line
	6050 1650 6100 1650
Wire Wire Line
	6050 1750 6100 1750
Entry Bus Bus
	6200 1850 6300 1950
Wire Wire Line
	9300 2550 9300 3100
Wire Wire Line
	9200 2550 9200 2900
Wire Wire Line
	9100 2550 9100 5400
Wire Wire Line
	8800 2550 8800 3000
Wire Wire Line
	8900 2550 8900 3800
Text Notes 5450 3600 2    50   ~ 0
Black
Text Notes 5450 3500 2    50   ~ 0
Red
Text Notes 5450 3400 2    50   ~ 0
White
Text Notes 5450 3300 2    50   ~ 0
Yellow
Text Notes 5450 3200 2    50   ~ 0
Orange
Text Notes 5450 3100 2    50   ~ 0
Green
Text Notes 5450 3000 2    50   ~ 0
Blue
Text Notes 9400 2650 0    50   ~ 0
Hardwired\nto relays
Wire Wire Line
	7800 3000 8800 3000
Wire Wire Line
	7800 3800 8900 3800
Wire Wire Line
	7800 5400 9100 5400
Wire Wire Line
	8100 2900 9200 2900
Wire Wire Line
	8200 3100 9300 3100
Wire Wire Line
	6050 3000 6800 3000
Wire Notes Line
	9800 2350 9800 5750
Wire Notes Line
	5800 2350 9800 2350
Wire Notes Line
	5800 5750 9800 5750
NoConn ~ 2000 6300
NoConn ~ 2000 6800
NoConn ~ 2000 5800
NoConn ~ 2000 5300
NoConn ~ 2000 4800
NoConn ~ 2000 4300
NoConn ~ 2000 3800
NoConn ~ 2000 3300
NoConn ~ 2000 2800
NoConn ~ 2000 2300
NoConn ~ 2000 1750
NoConn ~ 2000 1250
Text Notes 2200 6700 0    50   ~ 0
black
Text Notes 2200 6600 0    50   ~ 0
blue
Text Notes 2200 6500 0    50   ~ 0
yellow
Text Notes 2200 6400 0    50   ~ 0
red
Text Notes 2200 4700 0    50   ~ 0
red*
Text Notes 2200 3500 0    50   ~ 0
red*
Text Notes 2200 2700 0    50   ~ 0
blue
Text Notes 2200 1550 0    50   ~ 0
violet
Text Notes 2200 5500 0    50   ~ 0
white
Text Notes 2200 5400 0    50   ~ 0
white
Text Notes 2200 4600 0    50   ~ 0
orange
Text Notes 2200 4500 0    50   ~ 0
red*
Text Notes 2200 4400 0    50   ~ 0
yellow
Text Notes 2200 3600 0    50   ~ 0
green
Text Notes 2200 3700 0    50   ~ 0
blue
Text Notes 2200 3400 0    50   ~ 0
orange
Text Notes 2200 2600 0    50   ~ 0
blue
Text Notes 2200 2500 0    50   ~ 0
red*
Text Notes 2200 2400 0    50   ~ 0
green
Text Notes 2200 1450 0    50   ~ 0
red*
Wire Wire Line
	6350 3500 6350 5400
Wire Wire Line
	6450 5500 6900 5500
Wire Wire Line
	6450 3400 6450 5500
Wire Wire Line
	6900 5400 6350 5400
Connection ~ 6350 5400
Wire Wire Line
	6350 5400 6350 6300
Text Notes 2200 5700 0    50   ~ 0
black
Text Notes 1050 7950 0    50   ~ 0
* The red leads (+3.3v) on these jacks are wired to “black” pins.\n   I had wired them with black (ground) initially but that turned out to\n   be in error and it was easier to just change the color than rewire\n   the whole thing.
Wire Bus Line
	6300 1950 10500 1950
Wire Wire Line
	4350 3600 5500 3600
Wire Wire Line
	4250 3500 5500 3500
Wire Wire Line
	4150 3400 5500 3400
Wire Wire Line
	4050 3300 5500 3300
Wire Wire Line
	3950 3200 5500 3200
Wire Wire Line
	3950 3100 5500 3100
Wire Wire Line
	3850 3000 5500 3000
Wire Wire Line
	3550 1450 5500 1450
Wire Wire Line
	3450 1350 5500 1350
Wire Wire Line
	3350 1250 5500 1250
Wire Wire Line
	3250 1150 5500 1150
Wire Wire Line
	3150 1050 5500 1050
Text Notes 2250 7550 0    50   ~ 0
Park Wiring\n5: +12v\n4: D0 digital out @5v\n3: A0 analog out @5v\n2: Ground
Wire Notes Line
	2750 750  5750 750 
Wire Notes Line
	2750 7050 5750 7050
Wire Wire Line
	2000 5500 3650 5500
Wire Wire Line
	2000 5700 4350 5700
$Comp
L Connector:6P6C J4
U 1 1 609A144B
P 1600 1550
F 0 "J4" H 1200 1550 50  0000 C CNN
F 1 "WX" H 1657 2026 50  0000 C CNN
F 2 "" V 1600 1575 50  0001 C CNN
F 3 "~" V 1600 1575 50  0001 C CNN
	1    1600 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 1550 3150 1050
Wire Wire Line
	3050 1450 3050 1650
Connection ~ 3050 1650
Wire Wire Line
	3050 1650 3050 2500
$Comp
L Device:R R201
U 1 1 61484A1B
P 7800 4700
F 0 "R201" V 7900 4700 50  0000 C CNN
F 1 "1K" V 7684 4700 50  0000 C CNN
F 2 "" V 7730 4700 50  0001 C CNN
F 3 "~" H 7800 4700 50  0001 C CNN
	1    7800 4700
	0    1    1    0   
$EndComp
$Comp
L Isolator:4N35 U8
U 1 1 614862EC
P 7350 4600
F 0 "U8" H 7500 4800 50  0000 C CNN
F 1 "4N35" H 7250 4800 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 7150 4400 50  0001 L CIN
F 3 "https://www.vishay.com/docs/81181/4n35.pdf" H 7350 4600 50  0001 L CNN
	1    7350 4600
	-1   0    0    1   
$EndComp
Wire Wire Line
	8100 3700 8100 5300
Wire Wire Line
	8200 3900 8200 4500
Wire Wire Line
	9000 2550 9000 4700
Connection ~ 8200 4500
Wire Wire Line
	8200 4500 8200 5500
Wire Wire Line
	6550 3300 6550 4600
NoConn ~ 7050 4700
$Comp
L relay_module:Relay_Module-myLib K1
U 1 1 614842C8
P 7350 2950
F 0 "K1" H 7350 3225 50  0000 C CNN
F 1 "Roof" H 7350 3134 50  0000 C CNN
F 2 "" H 7350 2950 50  0001 C CNN
F 3 "" H 7350 2950 50  0001 C CNN
	1    7350 2950
	-1   0    0    -1  
$EndComp
$Comp
L relay_module:Relay_Module-myLib K2
U 1 1 61499AEE
P 7350 3750
F 0 "K2" H 7350 4025 50  0000 C CNN
F 1 "Mount" H 7350 3934 50  0000 C CNN
F 2 "" H 7350 3750 50  0001 C CNN
F 3 "" H 7350 3750 50  0001 C CNN
	1    7350 3750
	-1   0    0    -1  
$EndComp
$Comp
L relay_module:Relay_Module-myLib K3
U 1 1 614C0E5F
P 7350 5350
F 0 "K3" H 7350 5625 50  0000 C CNN
F 1 "Laser" H 7350 5550 50  0000 C CNN
F 2 "" H 7350 5350 50  0001 C CNN
F 3 "" H 7350 5350 50  0001 C CNN
	1    7350 5350
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7950 4700 9000 4700
Wire Wire Line
	8200 4500 7650 4500
Wire Wire Line
	6550 4600 7050 4600
Wire Wire Line
	6800 4500 7050 4500
Wire Notes Line
	7000 4850 7950 4850
Text Notes 7300 4350 0    50   ~ 0
FOB
Wire Notes Line
	7000 4400 7950 4400
Wire Notes Line
	7000 4400 7000 4850
Wire Notes Line
	7950 4400 7950 4850
Wire Wire Line
	3650 1550 5500 1550
Wire Wire Line
	3650 1550 3650 5500
Wire Wire Line
	3050 1650 5500 1650
Wire Wire Line
	3050 5600 3050 4700
Connection ~ 3050 4700
Wire Wire Line
	2000 5600 3050 5600
Wire Bus Line
	8900 2450 10500 2450
Wire Bus Line
	6200 1150 6200 1850
$EndSCHEMATC
