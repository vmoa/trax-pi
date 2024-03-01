EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 1
Title "T-Rax Control Board"
Date "2021-10-31"
Rev "v1.7"
Comp "Robert Ferguson Observatory"
Comment1 "David Kensiski"
Comment2 "v1.5 remove park isolator (see detector module); replace fob relay with isolator"
Comment3 "v1.6 merge all schematics into one doc; add accessory modules"
Comment4 "v1.7 direct wire fob isolator to fob trigger "
$EndDescr
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
L Regulator_Linear:LM1084-ADJ U?
U 1 1 65EBE818
P 3700 4150
AR Path="/61524F60/65EBE818" Ref="U?"  Part="1" 
AR Path="/65EBE818" Ref="U1"  Part="1" 
F 0 "U1" V 3550 3850 50  0000 L CNN
F 1 "LM1084" H 3550 4300 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220F-3_Vertical" H 3700 4400 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm1084.pdf" H 3700 4150 50  0001 C CNN
	1    3700 4150
	0    -1   -1   0   
$EndComp
$Comp
L Connector:6P6C J?
U 1 1 65EBE81E
P 3900 5300
AR Path="/61524F60/65EBE81E" Ref="J?"  Part="1" 
AR Path="/65EBE81E" Ref="J1"  Part="1" 
F 0 "J1" V 4000 4950 50  0000 R CNN
F 1 "RJ25" V 3900 4950 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" V 3900 5325 50  0001 C CNN
F 3 "~" V 3900 5325 50  0001 C CNN
	1    3900 5300
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3700 3850 3700 3800
$Comp
L Device:R R?
U 1 1 65EBE825
P 3850 3800
AR Path="/61524F60/65EBE825" Ref="R?"  Part="1" 
AR Path="/65EBE825" Ref="R1"  Part="1" 
F 0 "R1" V 3643 3800 50  0000 C CNN
F 1 "118" V 3734 3800 50  0000 C CNN
F 2 "Resistor_THT:R_Box_L8.4mm_W2.5mm_P5.08mm" V 3780 3800 50  0001 C CNN
F 3 "~" H 3850 3800 50  0001 C CNN
	1    3850 3800
	0    1    1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 65EBE82B
P 4150 3800
AR Path="/61524F60/65EBE82B" Ref="R?"  Part="1" 
AR Path="/65EBE82B" Ref="R2"  Part="1" 
F 0 "R2" V 3943 3800 50  0000 C CNN
F 1 "354" V 4034 3800 50  0000 C CNN
F 2 "Resistor_THT:R_Box_L8.4mm_W2.5mm_P5.08mm" V 4080 3800 50  0001 C CNN
F 3 "~" H 4150 3800 50  0001 C CNN
	1    4150 3800
	0    1    1    0   
$EndComp
Wire Wire Line
	4000 4150 4000 3800
Connection ~ 4000 3800
Connection ~ 3700 3800
NoConn ~ 4500 2600
NoConn ~ 4100 4900
NoConn ~ 3600 4900
Text Notes 4000 2850 0    50   ~ 0
5V
Wire Notes Line
	3300 1500 3300 5700
Wire Notes Line
	5450 5700 5450 1500
Wire Notes Line
	3300 5700 5450 5700
Wire Notes Line
	3300 1500 5450 1500
Text Notes 3850 1400 0    100  ~ 0
Park Detector
Text Notes 3500 4650 0    50   ~ 0
12V
$Comp
L photo_detector_module:Photo_Detector_Module X?
U 1 1 65EBE83E
P 4350 2100
AR Path="/61524F60/65EBE83E" Ref="X?"  Part="1" 
AR Path="/65EBE83E" Ref="X1"  Part="1" 
F 0 "X1" V 4700 2400 50  0000 L CNN
F 1 "Photo Detector Module" V 4800 1650 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PhotoDetectorModule" H 4450 2050 50  0001 C CNN
F 3 "" H 4450 2050 50  0001 C CNN
	1    4350 2100
	0    1    -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 65EBE844
P 4600 3250
AR Path="/61524F60/65EBE844" Ref="R?"  Part="1" 
AR Path="/65EBE844" Ref="R3"  Part="1" 
F 0 "R3" V 4700 3150 50  0000 C CNN
F 1 "1K" V 4500 3250 50  0000 C CNN
F 2 "Resistor_THT:R_Box_L8.4mm_W2.5mm_P5.08mm" V 4530 3250 50  0001 C CNN
F 3 "~" H 4600 3250 50  0001 C CNN
	1    4600 3250
	0    1    1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 65EBE84A
P 4850 2900
AR Path="/61524F60/65EBE84A" Ref="R?"  Part="1" 
AR Path="/65EBE84A" Ref="R4"  Part="1" 
F 0 "R4" V 4800 3100 50  0000 C CNN
F 1 "1K" V 4950 2900 50  0000 C CNN
F 2 "Resistor_THT:R_Box_L8.4mm_W2.5mm_P5.08mm" V 4780 2900 50  0001 C CNN
F 3 "~" H 4850 2900 50  0001 C CNN
	1    4850 2900
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 65EBE850
P 5250 4100
AR Path="/61524F60/65EBE850" Ref="R?"  Part="1" 
AR Path="/65EBE850" Ref="R5"  Part="1" 
F 0 "R5" H 5150 4200 50  0000 C CNN
F 1 "100" H 5100 4050 50  0000 C CNN
F 2 "Resistor_THT:R_Box_L8.4mm_W2.5mm_P5.08mm" V 5180 4100 50  0001 C CNN
F 3 "~" H 5250 4100 50  0001 C CNN
	1    5250 4100
	1    0    0    1   
$EndComp
$Comp
L Isolator:4N25 U?
U 1 1 65EBE856
P 4850 4700
AR Path="/61524F60/65EBE856" Ref="U?"  Part="1" 
AR Path="/65EBE856" Ref="U2"  Part="1" 
F 0 "U2" H 4850 4500 50  0000 C CNN
F 1 "4N25" H 4850 4900 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 4650 4500 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 4850 4700 50  0001 L CNN
	1    4850 4700
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3900 4800 3900 4900
Connection ~ 4300 3800
Wire Wire Line
	4200 2600 4200 2900
Wire Wire Line
	5000 2900 5050 2900
Wire Wire Line
	5050 2900 5050 3050
Wire Wire Line
	5050 3450 5050 3550
Wire Wire Line
	4300 3800 4300 4400
Wire Wire Line
	5250 4600 5150 4600
Wire Wire Line
	5150 4800 5250 4800
Wire Wire Line
	4000 4400 4300 4400
Wire Wire Line
	4000 4400 4000 4900
Wire Wire Line
	3900 4800 4550 4800
Wire Wire Line
	3800 4900 3800 4700
Wire Wire Line
	3800 4700 4550 4700
$Comp
L power:GND #PWR?
U 1 1 65EBE86A
P 4300 4400
AR Path="/61524F60/65EBE86A" Ref="#PWR?"  Part="1" 
AR Path="/65EBE86A" Ref="#PWR0101"  Part="1" 
F 0 "#PWR0101" H 4300 4150 50  0001 C CNN
F 1 "GND" H 4305 4227 50  0000 C CNN
F 2 "" H 4300 4400 50  0001 C CNN
F 3 "" H 4300 4400 50  0001 C CNN
	1    4300 4400
	1    0    0    -1  
$EndComp
Connection ~ 4300 4400
$Comp
L power:GND #PWR?
U 1 1 65EBE871
P 5050 3550
AR Path="/61524F60/65EBE871" Ref="#PWR?"  Part="1" 
AR Path="/65EBE871" Ref="#PWR0102"  Part="1" 
F 0 "#PWR0102" H 5050 3300 50  0001 C CNN
F 1 "GND" H 5055 3377 50  0000 C CNN
F 2 "" H 5050 3550 50  0001 C CNN
F 3 "" H 5050 3550 50  0001 C CNN
	1    5050 3550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 65EBE877
P 5250 4800
AR Path="/61524F60/65EBE877" Ref="#PWR?"  Part="1" 
AR Path="/65EBE877" Ref="#PWR0103"  Part="1" 
F 0 "#PWR0103" H 5250 4550 50  0001 C CNN
F 1 "GND" H 5255 4627 50  0000 C CNN
F 2 "" H 5250 4800 50  0001 C CNN
F 3 "" H 5250 4800 50  0001 C CNN
	1    5250 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4300 2600 4300 3800
Wire Wire Line
	5250 4250 5250 4600
$Comp
L Transistor_BJT:2N2219 Q?
U 1 1 65EBE87F
P 4950 3250
AR Path="/61524F60/65EBE87F" Ref="Q?"  Part="1" 
AR Path="/65EBE87F" Ref="Q1"  Part="1" 
F 0 "Q1" H 4800 3400 50  0000 L CNN
F 1 "2N2222" H 4700 3100 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 5150 3175 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 4950 3250 50  0001 L CNN
	1    4950 3250
	1    0    0    -1  
$EndComp
NoConn ~ 4550 4600
Wire Wire Line
	3700 4450 3700 4900
Connection ~ 5050 2900
Wire Wire Line
	5050 2900 5250 2900
Wire Wire Line
	5250 3950 5250 2900
Wire Wire Line
	4400 3250 4450 3250
Wire Wire Line
	4400 2600 4400 3250
Wire Wire Line
	3700 2900 4200 2900
Connection ~ 4200 2900
Wire Wire Line
	4700 2900 4200 2900
Wire Wire Line
	3700 2900 3700 3800
Text Notes 4650 3550 0    50   ~ 0
(inverter)
Text Notes 3350 5950 0    50   ~ 0
NOTE: Park Laser and Detector are wired alike and should\nconnect to the “Park” port through an RJ11 splitter
$EndSCHEMATC
