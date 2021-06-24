EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 1
Title "T-Rax Relays & Connector wiring"
Date "2021-05-22"
Rev "v1.2b"
Comp "Robert Ferguson Observatory"
Comment1 "David Kensiski"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 4500 1050 2    50   ~ 0
Violet
Text Notes 4500 1750 2    50   ~ 0
Black
Text Notes 4500 1650 2    50   ~ 0
Red
Text Notes 4500 1550 2    50   ~ 0
White
Text Notes 4500 1450 2    50   ~ 0
Yellow
Text Notes 4500 1350 2    50   ~ 0
Orange
Text Notes 4500 1250 2    50   ~ 0
Green
Text Notes 4500 1150 2    50   ~ 0
Blue
Entry Wire Line
	8050 2550 8150 2450
Entry Wire Line
	8250 2450 8150 2550
Entry Wire Line
	8350 2450 8250 2550
Entry Wire Line
	8050 2450 7950 2550
Entry Wire Line
	7950 2450 7850 2550
Entry Wire Line
	8450 2450 8350 2550
Text Notes 8350 2600 3    50   ~ 0
Black
Text Notes 8250 2600 3    50   ~ 0
Red
Text Notes 8150 2600 3    50   ~ 0
White
Text Notes 8050 2600 3    50   ~ 0
Yellow
Text Notes 7950 2600 3    50   ~ 0
Orange
Text Notes 7850 2600 3    50   ~ 0
Green
$Comp
L Connector:6P6C J1
U 1 1 609A144B
P 1600 1600
F 0 "J1" H 1200 1600 50  0000 C CNN
F 1 "WX" H 1657 2076 50  0000 C CNN
F 2 "" V 1600 1625 50  0001 C CNN
F 3 "~" V 1600 1625 50  0001 C CNN
	1    1600 1600
	1    0    0    -1  
$EndComp
$Comp
L Connector:6P6C J3
U 1 1 609A2420
P 1600 3600
F 0 "J3" H 1200 3600 50  0000 C CNN
F 1 "MountPower" H 1657 4076 50  0000 C CNN
F 2 "" V 1600 3625 50  0001 C CNN
F 3 "~" V 1600 3625 50  0001 C CNN
	1    1600 3600
	1    0    0    -1  
$EndComp
$Comp
L Connector:6P6C J2
U 1 1 609A2BC1
P 1600 2600
F 0 "J2" H 1200 2600 50  0000 C CNN
F 1 "RoofPower" H 1657 3076 50  0000 C CNN
F 2 "" V 1600 2625 50  0001 C CNN
F 3 "~" V 1600 2625 50  0001 C CNN
	1    1600 2600
	1    0    0    -1  
$EndComp
$Comp
L Connector:6P6C J4
U 1 1 609A37E0
P 1600 4600
F 0 "J4" H 1200 4600 50  0000 C CNN
F 1 "Open/Close" H 1657 5076 50  0000 C CNN
F 2 "" V 1600 4625 50  0001 C CNN
F 3 "~" V 1600 4625 50  0001 C CNN
	1    1600 4600
	1    0    0    -1  
$EndComp
$Comp
L Connector:6P6C J5
U 1 1 609A462B
P 1600 5600
F 0 "J5" H 1200 5600 50  0000 C CNN
F 1 "Parked" H 1657 6076 50  0000 C CNN
F 2 "" V 1600 5625 50  0001 C CNN
F 3 "~" V 1600 5625 50  0001 C CNN
	1    1600 5600
	1    0    0    -1  
$EndComp
$Comp
L TRax-Relays-rescue:Relay_Module-myLib K1
U 1 1 609A763A
P 6400 2950
F 0 "K1" H 6400 3225 50  0000 C CNN
F 1 "Roof" H 6400 3134 50  0000 C CNN
F 2 "" H 6400 2950 50  0001 C CNN
F 3 "" H 6400 2950 50  0001 C CNN
	1    6400 2950
	-1   0    0    -1  
$EndComp
$Comp
L TRax-Relays-rescue:Relay_Module-myLib K2
U 1 1 609A9B89
P 6400 3750
F 0 "K2" H 6400 4025 50  0000 C CNN
F 1 "Mount" H 6400 3934 50  0000 C CNN
F 2 "" H 6400 3750 50  0001 C CNN
F 3 "" H 6400 3750 50  0001 C CNN
	1    6400 3750
	-1   0    0    -1  
$EndComp
$Comp
L TRax-Relays-rescue:Relay_Module-myLib K3
U 1 1 609AA6A6
P 6400 4550
F 0 "K3" H 6400 4825 50  0000 C CNN
F 1 "Fob" H 6400 4734 50  0000 C CNN
F 2 "" H 6400 4550 50  0001 C CNN
F 3 "" H 6400 4550 50  0001 C CNN
	1    6400 4550
	-1   0    0    -1  
$EndComp
$Comp
L TRax-Relays-rescue:Relay_Module-myLib K4
U 1 1 609AAFF2
P 6400 5350
F 0 "K4" H 6400 5625 50  0000 C CNN
F 1 "Laser" H 6400 5534 50  0000 C CNN
F 2 "" H 6400 5350 50  0001 C CNN
F 3 "" H 6400 5350 50  0001 C CNN
	1    6400 5350
	-1   0    0    -1  
$EndComp
Text Notes 1050 7550 0    50   ~ 0
RJ Color Code: Telco (Cat5)\n5. Yellow (Orange/White)\n4. Green  (White/Blue)\n3. Red    (Blue/White)\n2. Black  (White/Orange
Wire Wire Line
	2000 1600 3150 1600
Wire Wire Line
	2000 2600 3250 2600
Wire Wire Line
	2000 3600 3350 3600
Wire Wire Line
	2000 4600 3450 4600
Wire Wire Line
	2000 4400 3550 4400
Wire Wire Line
	2000 5600 3650 5600
Text Notes 10050 2450 2    50   ~ 0
Outputs from\nControl Board
Text Notes 10050 1950 2    50   ~ 0
Inputs from\nControl Board
Wire Wire Line
	6850 2900 7150 2900
Wire Wire Line
	6850 3100 7250 3100
Wire Wire Line
	7150 2900 7150 3700
Wire Wire Line
	7150 5300 6850 5300
Connection ~ 7150 2900
Wire Wire Line
	7250 3100 7250 3900
Wire Wire Line
	7250 5500 6850 5500
Connection ~ 7250 3100
Wire Wire Line
	6850 4500 7150 4500
Connection ~ 7150 4500
Wire Wire Line
	7150 4500 7150 5300
Wire Wire Line
	6850 4700 7250 4700
Connection ~ 7250 4700
Wire Wire Line
	7250 4700 7250 5500
Wire Wire Line
	6850 3700 7150 3700
Connection ~ 7150 3700
Wire Wire Line
	7150 3700 7150 4500
Wire Wire Line
	6850 3900 7250 3900
Connection ~ 7250 3900
Wire Wire Line
	7250 3900 7250 4700
$Comp
L power:+12V #PWR0101
U 1 1 60A1C6F9
P 5400 7100
F 0 "#PWR0101" H 5400 6950 50  0001 C CNN
F 1 "+12V" H 5300 7150 50  0000 C CNN
F 2 "" H 5400 7100 50  0001 C CNN
F 3 "" H 5400 7100 50  0001 C CNN
	1    5400 7100
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 60A26175
P 5300 7100
F 0 "#PWR0102" H 5300 6850 50  0001 C CNN
F 1 "GND" H 5150 7050 50  0000 C CNN
F 2 "" H 5300 7100 50  0001 C CNN
F 3 "" H 5300 7100 50  0001 C CNN
	1    5300 7100
	1    0    0    -1  
$EndComp
NoConn ~ 5950 2900
NoConn ~ 5950 3700
NoConn ~ 5950 4500
NoConn ~ 5950 5300
NoConn ~ 2000 1700
NoConn ~ 2000 1400
Wire Wire Line
	5950 3800 5850 3800
Wire Wire Line
	5950 4600 5850 4600
Wire Wire Line
	2000 5400 4150 5400
Wire Wire Line
	5950 4700 5600 4700
$Comp
L Connector:6P6C J6
U 1 1 609A546C
P 1600 6600
F 0 "J6" H 1200 6600 50  0000 C CNN
F 1 "Fob" H 1657 7076 50  0000 C CNN
F 2 "" V 1600 6625 50  0001 C CNN
F 3 "~" V 1600 6625 50  0001 C CNN
	1    1600 6600
	1    0    0    -1  
$EndComp
Text Notes 3400 5400 2    50   ~ 0
12V switched
Wire Wire Line
	2000 5700 4350 5700
Wire Wire Line
	2000 2400 3950 2400
Wire Wire Line
	2000 3400 3950 3400
Wire Wire Line
	5850 3000 5950 3000
Connection ~ 5850 3800
Wire Wire Line
	5850 3800 5850 4600
Wire Wire Line
	2000 6500 4050 6500
$Comp
L Connector:Conn_01x07_Male J10
U 1 1 60B04D3A
P 4900 3300
F 0 "J10" H 4950 2800 50  0000 C CNN
F 1 "Relays" H 5000 2900 50  0000 C CNN
F 2 "" H 4900 3300 50  0001 C CNN
F 3 "~" H 4900 3300 50  0001 C CNN
	1    4900 3300
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x07_Male J8
U 1 1 60AFF249
P 4750 3300
F 0 "J8" H 4900 2800 50  0000 R CNN
F 1 "Relays" H 5000 2900 50  0000 R CNN
F 2 "" H 4750 3300 50  0001 C CNN
F 3 "~" H 4750 3300 50  0001 C CNN
	1    4750 3300
	-1   0    0    -1  
$EndComp
Connection ~ 5850 3000
Wire Wire Line
	5100 3100 5950 3100
Wire Wire Line
	5850 3000 5850 3800
Wire Wire Line
	5700 3200 5700 3900
Wire Wire Line
	5100 3200 5700 3200
Wire Wire Line
	5700 3900 5950 3900
Wire Wire Line
	5100 3300 5600 3300
Wire Wire Line
	5600 3300 5600 4700
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
	5100 3400 5500 3400
Wire Wire Line
	4150 3400 4150 5400
Wire Wire Line
	2000 6700 4350 6700
Wire Wire Line
	5100 3500 5400 3500
Wire Wire Line
	5100 3600 5300 3600
Wire Wire Line
	5300 3600 5300 7100
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
	3950 3100 4550 3100
Wire Wire Line
	3850 2700 3850 3000
Connection ~ 3850 3000
Wire Wire Line
	3850 3000 3850 3700
Wire Wire Line
	3950 3200 4550 3200
Wire Wire Line
	4150 3400 4550 3400
Wire Wire Line
	4350 3600 4550 3600
Wire Notes Line
	4850 5750 4850 2350
Text Notes 5600 2500 2    79   ~ 0
Relay Board
Wire Wire Line
	4550 3000 3850 3000
Wire Wire Line
	4550 3300 4050 3300
Wire Wire Line
	4550 3500 4250 3500
$Comp
L Connector:Conn_01x08_Male J7
U 1 1 6105C513
P 4750 1350
F 0 "J7" H 4900 750 50  0000 R CNN
F 1 "Inputs" H 5050 850 50  0000 R CNN
F 2 "" H 4750 1350 50  0001 C CNN
F 3 "~" H 4750 1350 50  0001 C CNN
	1    4750 1350
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3250 1150 4550 1150
Wire Wire Line
	3350 1250 4550 1250
Wire Wire Line
	3450 1350 4550 1350
Wire Wire Line
	3550 1450 4550 1450
Wire Wire Line
	3650 1550 4550 1550
NoConn ~ 4550 1650
Wire Wire Line
	3650 1550 3650 5600
Wire Wire Line
	3550 1450 3550 4400
Wire Wire Line
	3450 1350 3450 4600
Wire Wire Line
	3350 1250 3350 3600
Wire Wire Line
	3250 1150 3250 2600
Wire Wire Line
	3150 1600 3150 1050
Wire Wire Line
	3150 1050 4550 1050
Wire Wire Line
	3050 1500 3050 1750
Wire Wire Line
	2000 5500 3050 5500
Wire Wire Line
	2000 1500 3050 1500
Wire Wire Line
	4550 1750 3050 1750
Connection ~ 3050 1750
Wire Wire Line
	3050 1750 3050 2500
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
Connection ~ 3050 4700
Wire Wire Line
	3050 4700 3050 5500
Wire Notes Line
	4800 750  2750 750 
Wire Notes Line
	2750 750  2750 7050
Wire Notes Line
	2750 7050 4800 7050
Wire Notes Line
	4800 750  4800 7050
Text Notes 3800 900  2    79   ~ 0
Connector Board
Entry Wire Line
	5250 1850 5150 1750
Entry Wire Line
	5250 1150 5150 1050
Entry Wire Line
	5250 1250 5150 1150
Entry Wire Line
	5250 1350 5150 1250
Entry Wire Line
	5250 1450 5150 1350
Entry Wire Line
	5250 1550 5150 1450
Entry Wire Line
	5250 1650 5150 1550
Entry Wire Line
	5250 1750 5150 1650
$Comp
L Connector_Generic:Conn_01x08 J9
U 1 1 611FE672
P 4900 1350
F 0 "J9" H 4818 1775 50  0001 C CNN
F 1 "Conn_01x08" H 4818 1776 50  0001 C CNN
F 2 "" H 4900 1350 50  0001 C CNN
F 3 "~" H 4900 1350 50  0001 C CNN
	1    4900 1350
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5100 1050 5150 1050
Wire Wire Line
	5100 1150 5150 1150
Wire Wire Line
	5100 1250 5150 1250
Wire Wire Line
	5100 1350 5150 1350
Wire Wire Line
	5100 1450 5150 1450
Wire Wire Line
	5100 1550 5150 1550
Wire Wire Line
	5100 1650 5150 1650
Wire Wire Line
	5100 1750 5150 1750
Entry Bus Bus
	5250 1850 5350 1950
Wire Wire Line
	8350 2550 8350 3100
Wire Wire Line
	8250 2550 8250 2900
Wire Wire Line
	8150 2550 8150 5400
Wire Wire Line
	8050 2550 8050 4600
Wire Wire Line
	7850 2550 7850 3000
Wire Wire Line
	7950 2550 7950 3800
Text Notes 4500 3600 2    50   ~ 0
Black
Text Notes 4500 3500 2    50   ~ 0
Red
Text Notes 4500 3400 2    50   ~ 0
White
Text Notes 4500 3300 2    50   ~ 0
Yellow
Text Notes 4500 3200 2    50   ~ 0
Orange
Text Notes 4500 3100 2    50   ~ 0
Green
Text Notes 4500 3000 2    50   ~ 0
Blue
Text Notes 8900 2700 0    50   ~ 0
Hardwired\non relay\nboard
Wire Wire Line
	6850 3000 7850 3000
Wire Wire Line
	6850 3800 7950 3800
Wire Wire Line
	6850 4600 8050 4600
Wire Wire Line
	6850 5400 8150 5400
Wire Wire Line
	7150 2900 8250 2900
Wire Wire Line
	7250 3100 8350 3100
Wire Wire Line
	5100 3000 5850 3000
Wire Notes Line
	8850 2350 8850 5750
Wire Notes Line
	4850 2350 8850 2350
Wire Notes Line
	4850 5750 8850 5750
Wire Bus Line
	5350 1950 10100 1950
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
NoConn ~ 2000 1800
NoConn ~ 2000 1300
Text Notes 2200 6700 0    50   ~ 0
black
Text Notes 2200 6600 0    50   ~ 0
blue
Text Notes 2200 6500 0    50   ~ 0
yellow
Text Notes 2200 6400 0    50   ~ 0
red
Text Notes 2200 5700 0    50   ~ 0
black
Text Notes 2200 4700 0    50   ~ 0
black
Text Notes 2200 3500 0    50   ~ 0
black
Text Notes 2200 2700 0    50   ~ 0
blue
Text Notes 2200 1600 0    50   ~ 0
violet
Text Notes 2200 5600 0    50   ~ 0
white
Text Notes 2200 5500 0    50   ~ 0
black
Text Notes 2200 5400 0    50   ~ 0
white
Text Notes 2200 4600 0    50   ~ 0
orange
Text Notes 2200 4500 0    50   ~ 0
black
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
black
Text Notes 2200 2400 0    50   ~ 0
green
Text Notes 2200 1500 0    50   ~ 0
black
Wire Wire Line
	5400 3500 5400 5400
Wire Wire Line
	5500 5500 5950 5500
Wire Wire Line
	5500 3400 5500 5500
Wire Wire Line
	5950 5400 5400 5400
Connection ~ 5400 5400
Wire Wire Line
	5400 5400 5400 7100
Wire Bus Line
	7950 2450 10100 2450
Wire Bus Line
	5250 1150 5250 1850
$EndSCHEMATC
