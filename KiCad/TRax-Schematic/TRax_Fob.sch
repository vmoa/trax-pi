EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 3 4
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:RJ25 J?
U 1 1 6147FB50
P 2500 2800
F 0 "J?" H 2557 3367 50  0000 C CNN
F 1 "RJ25" H 2557 3276 50  0000 C CNN
F 2 "" V 2500 2825 50  0001 C CNN
F 3 "~" V 2500 2825 50  0001 C CNN
	1    2500 2800
	1    0    0    -1  
$EndComp
$Comp
L Device:FOB X?
U 1 1 615205D5
P 4400 2650
F 0 "X?" H 4778 2726 50  0000 L CNN
F 1 "FOB" H 4778 2635 50  0000 L CNN
F 2 "" H 4450 2750 50  0001 C CNN
F 3 "" H 4450 2750 50  0001 C CNN
	1    4400 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2900 2700 4150 2700
Wire Wire Line
	2900 2800 4150 2800
Wire Wire Line
	2900 2900 3650 2900
Wire Wire Line
	3650 2900 3650 2550
Wire Wire Line
	3650 2550 4150 2550
Wire Wire Line
	2900 2600 3550 2600
Wire Wire Line
	3550 2600 3550 2450
Wire Wire Line
	3550 2450 4150 2450
Text Notes 2950 2600 0    50   ~ 0
Yellow
Text Notes 2950 2700 0    50   ~ 0
Green
Text Notes 2950 2800 0    50   ~ 0
Red
Text Notes 2950 2900 0    50   ~ 0
Black
NoConn ~ 2900 2500
NoConn ~ 2900 3000
$EndSCHEMATC
