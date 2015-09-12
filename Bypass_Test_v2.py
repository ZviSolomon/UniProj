# dts_calc_avg.py skl - rsemman - version 1.0 - ww38 2014#
# ----------------------------------------------- #

import sys, evg



def BypassTest():
	#check if it is the first test to bypass
	evg.PrintToConsole("Start\n")
	
	a = evg.GetGSDSData("CurrentTestToBypass","string","LOT",-99,0)
	evg.PrintToConsole(a)
	evg.PrintToConsole("\n")
	
	if evg.GetGSDSData("CurrentTestToBypass","string","LOT",-99,0) == 'NoTestToBypass':  
		evg.PrintToConsole("if1\n")
		
		main_flow = open("D:/temp/mainFlow.txt", "r");
			
		testnames = [];
		ports = [];
			
		#insert test names and ports from txt file into array's 
		for line in main_flow:
			splited_line = line.split('##');
			testnames.append(splited_line[0]);
			ports.append(splited_line[1]);
			
		#i will help for iteration
		evg.SetGSDSIntData("i",0,"LOT",-99,0,1);
			
		#save the number of test names in txt file
		evg.SetGSDSIntData("testnames_num",len(testnames),"LOT",-99,0,1);
		testnum = evg.GetGSDSData("testnames_num","integer","LOT",-99,0)
		evg.PrintToConsole(str(testnum))
		evg.PrintToConsole("\n")
			
		#save current test name to bypass
		evg.SetGSDSStrData("CurrentTestToBypass",testnames[evg.GetGSDSData("i","integer","LOT",-99,0)],"LOT",-99,0,1);
		evg.PrintToConsole(evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0))
		evg.PrintToConsole("\n")
			
		#save sanity flag to determine how to un-bypass previous tests
		evg.SetGSDSIntData("SanityFlag",0,"LOT",-99,0,1);
		evg.PrintToConsole(str(evg.GetGSDSData("SanityFlag","integer","LOT",-99,0)))
		evg.PrintToConsole("\n")
		
			
		#check if CurrentTestToBypass is already bypassed by default - then do nothing, just continue
		try:
			if (int(evg.GetTestParam(evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0), "bypass_global")) == -1):
				#bypass the first test name
				evg.PrintToConsole("if2\n")
				evg.SetTestParamStr(evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0), "bypass_global", str(ports[evg.GetGSDSData("i","integer","LOT",-99,0)]));
				#print to ituff the test name being bypassed
				#CTTB_ituff = '2_tname_' + evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0) + 'bypass' + '\n2_mrslt_' + str(ports[evg.GetGSDSData("i","integer","LOT",-99,0)]) + '\n'
				CTTB_ituff = '2_tname_' + evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0) + 'bypass'
				evg.PrintToItuff(CTTB_ituff)
				evg.PrintToConsole(CTTB_ituff)
				PTC = str(evg.GetGSDSData("i","integer","LOT",-99,0)) + '_iteration_CTTB_bypass'
				evg.PrintToConsole(PTC)
				evg.SetGSDSIntData("SanityFlag",0,"LOT",-99,0,1);
				evg.SetSitePort(0,0)
				return
		except:
			evg.PrintToConsole("Empty Bypass")
			evg.PrintToConsole("\n")	
			evg.SetSitePort(0,0)
			return
			
		else:
			evg.PrintToConsole("else\n")
			#update sanity flag to 1 - mark this test for sanity check
			evg.SetGSDSIntData("SanityFlag",1,"LOT",-99,0,1);
			evg.PrintToConsole(str(evg.GetGSDSData("SanityFlag","integer","LOT",-99,0)))
			evg.PrintToConsole("\n")		
			PTC = str(evg.GetGSDSData("i","integer","LOT",-99,0)) + '_iteration_CTTB_bypass_default\n'
			evg.PrintToConsole(PTC)
			evg.SetSitePort(0,0)
			return		

		
	#check if we still have test names to bypass 
	elif evg.GetGSDSData("i","integer","LOT",-99,0) < (evg.GetGSDSData("testnames_num","integer","LOT",-99,0) - 1):
		
		evg.PrintToConsole("elif\n")
		main_flow = open("D:/temp/mainFlow.txt", "r");
			
		testnames = [];
		ports = [];
			
		#insert test names and ports from txt file into array's 
		for line in main_flow:
			splited_line = line.split('##');
			testnames.append(splited_line[0]);
			ports.append(splited_line[1]);
		
		#un-bypass the previous test name
		if evg.GetGSDSData("SanityFlag","integer","LOT",-99,0) == 0:
			#only if previous test name was not already by-passed then un-bypass it 
			evg.SetTestParamStr(evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0), "bypass_global", "-1");
			evg.PrintToConsole("if1_elif\n")	
			
		#i = i + 1
		old_i = evg.GetGSDSData("i","integer","LOT",-99,0);
		evg.SetGSDSIntData("i",old_i+1,"LOT",-99,0,1);
			
		#set CurrentTestToBypass to the next test name
		evg.SetGSDSStrData("CurrentTestToBypass",testnames[evg.GetGSDSData("i","integer","LOT",-99,0)],"LOT",-99,0,1);
		evg.PrintToConsole(evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0))
		evg.PrintToConsole("\n")
			
		#bypass current test name (still check if it is not already bypassed by default)
		try:
			if (int(evg.GetTestParam(evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0), "bypass_global")) == -1):
				evg.PrintToConsole("if2_elif\n")
				evg.SetTestParamStr(evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0), "bypass_global", str(ports[evg.GetGSDSData("i","integer","LOT",-99,0)]));
				#print to ituff the test name being bypassed
				evg.PrintToConsole("if2_elif\n")
				#CTTB_ituff = '2_tname_' + evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0) + 'bypass' + '\n2_mrslt_' + str(ports[evg.GetGSDSData("i","integer","LOT",-99,0)]) + '\n'
				CTTB_ituff = '2_tname_' + evg.GetGSDSData("CurrentTestToBypass","string", "LOT", -99, 0) + 'bypass'
				evg.PrintToItuff(CTTB_ituff)
				evg.PrintToConsole(CTTB_ituff)
				PTC = str(evg.GetGSDSData("i","integer","LOT",-99,0)) + '_iteration_CTTB_bypass'
				evg.PrintToConsole(PTC)
				evg.SetGSDSIntData("SanityFlag",0,"LOT",-99,0,1);
				evg.SetSitePort(0,0)
				return
		except:
			evg.PrintToConsole("Empty Bypass")
			evg.PrintToConsole("\n")
			evg.SetSitePort(0,0)
			return
	
		else: 
			evg.PrintToConsole("else1_elif\n")
			#update sanity flag to 1 - mark this test for sanity check
			evg.SetGSDSIntData("SanityFlag",1,"LOT",-99,0,1);
			evg.PrintToConsole(str(evg.GetGSDSData("SanityFlag","integer","LOT",-99,0)))
			evg.PrintToConsole("\n")			
			PTC = str(evg.GetGSDSData("i","integer","LOT",-99,0)) + '_iteration_CTTB_bypass_default'
			evg.PrintToConsole(PTC)
			evg.SetSitePort(0,0)
			return

	else:
		evg.PrintToConsole("end_of_iteration\n")
		evg.SetSitePort(0,1)
		return
