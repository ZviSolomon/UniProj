# dts_calc_avg.py skl - rsemman - version 1.0 - ww38 2014#
# ----------------------------------------------- #

import evg 
import sys 

def InitBypass():
	PTC = 'inside_Bypass_Test_INIT\n'
	evg.PrintToConsole(PTC)
	evg.SetGSDSStrData("CurrentTestToBypass","NoTestToBypass","LOT",-99,0,1)
	a = evg.GetGSDSData("CurrentTestToBypass","string","LOT",-99,0)
	evg.PrintToConsole(a)
	evg.PrintToConsole("\n")
	return 1


