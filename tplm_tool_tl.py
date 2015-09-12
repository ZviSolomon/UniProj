#!/usr/bin/env python
# encoding: utf-8
# Filename: tpl_tool.py

'''
This script is used to modify tpl module port 0 connections.
  1. bypass all fork test instances.
'''
import sys
import re
from os.path import abspath, sep, isfile
from os import listdir, rename   # , remove
# from optparse import OptionParser
# import fileinput
# import ipdb


ignore_TI_list = [

]
ignore_MO_list = [
    "C_BASE_FLOWS",
    "C_THERMAL_DIODE_START_TDAU",
    "C_DCTEST_CONT_CPU",
    "C_DCTEST_SHOPS_CPU",
    "C_DCTEST_EDM",
    "C_THERMAL_DIODE_SOT_CPU",
    "C_FUSE_READ",
    "C_DFFREAD",
    "C_DCTEST_PCHCONT",
    "C_DCTEST_PCHEDM",
    "C_DCTEST_PCHSHOPS",
    "C_BASE_BIN",
    "C_PCHRESET",
    "C_THERMAL_SOT",
]
all_flows = ['MAIN', 'END', 'PWRDWN', 'DEDC', 'EDCFLOW', 'STATICFF']


def getTPLList(TPPath):
    """
    To get all tpl files from each module.
    SKL is simple since each module folder only
    contains one tpl file.
    """
    tpl_list = []
    ModulePath = abspath(TPPath) + sep + "Modules" + sep
    ModuleList = listdir(ModulePath)
    for module in ModuleList:
        module_files = listdir(abspath(ModulePath + module))
        temp_re = re.compile("\.tpl$")
        for file in module_files:
            if temp_re.search(file):
                tpl_list.append(ModulePath + module + sep + file)
    return sorted(tpl_list)  # Return full path of tpl file in each modules.


def tplmodify(oldtplfile, newtplfile, module, dutdict):
    '''
    To connect module's 0 port to next module.
    '''

    # Define regxp patterns
    dutflow_pa = re.compile('^DUTFlow\s+(\w*)')
    dutflowitem_pa = re.compile('^\sDUTFlowItem\s+(\w*)\s')
    port_pa = re.compile('Result\s+(-?\d+)')
    goto_pa = re.compile('(GoTo\s+(\w*))')
    return_pa = re.compile('(Return (\d))')
    r_brace_pa = re.compile(r'^\}')

    # Define global variables
    j = 0
    dutfi = {}
    dutf = {}
    dutf_flag = False

    # Open Files
    inputfile = open(oldtplfile, 'r')
    outputfile = open(newtplfile, 'w')

    for l in inputfile:
        j += 1
        # For debug purpose
        # if j == 661:
        #     print("Stop")
        if dutflow_pa.search(l):
            df = dutflow_pa.search(l).group(1)
            dutf_flag = True
        if dutflowitem_pa.search(l) and dutf_flag:
            dfi = dutflowitem_pa.search(l).group(1)
        if port_pa.search(l) and dutf_flag:
            pn = port_pa.search(l).group(1)
        if (goto_pa.search(l) or return_pa.search(l)) and dutf_flag:
            for fk in all_flows:
                flow_key = module + '_' + fk
                if flow_key in dutdict.keys():
                    if df in dutdict[flow_key].keys() and \
                       dfi not in dutdict[flow_key].keys():
                        for kp in sorted(dutdict[df][dfi].keys()):
                            if dutdict[df][dfi][kp][0] == 'Pass':
                                rep = dutdict[df][dfi][kp][3]
                                break
                        if dutdict[df][dfi][pn][0:3] == ('Fail', True, True):
                            if dfi not in ignore_TI_list:
                                try:
                                    l = l.replace(dutdict[df][dfi][pn][3], rep)
                                    del rep
                                except NameError:
                                    None
                    elif df == flow_key:
                        if dfi not in dutdict.keys():
                            for kp in sorted(dutdict[df][dfi].keys()):
                                if dutdict[df][dfi][kp][0] == 'Pass':
                                    rep = dutdict[df][dfi][kp][3]
                                    break
                            if dutdict[df][dfi][pn][0:3] == ('Fail',
                                                             True, True):
                                if dfi not in ignore_TI_list:
                                    try:
                                        l = l.replace(dutdict[df][dfi][pn][3],
                                                      rep)
                                        del rep
                                    except NameError:
                                        None
        if dutf_flag and r_brace_pa.search(l):
            dutf[df] = dutfi
            dutf_flag = False

        outputfile.write(l)

    outputfile.close()
    inputfile.close()


def parseTPL(tplfile):
    '''
    To connect module's 0 port to next module.
    '''

    # Define regxp patterns
    dutflow_pa = re.compile('^DUTFlow\s+(\w*)')
    dutflowitem_pa = re.compile('^\sDUTFlowItem\s+(\w*)\s')
    port_pa = re.compile('Result\s+(-?\d+)')
    pf_pa = re.compile(r'Property PassFail = "(\w*)"')
    counter_pa = re.compile(r'IncrementCounters')
    bin_pa = re.compile(r'SetBin')
    goto_pa = re.compile('(GoTo\s+(\w*))')
    return_pa = re.compile('(Return (\d))')
    r_brace_pa = re.compile(r'^\}')

    # Define global variables
    j = 0
    dutfi = {}
    dutf = {}
    dutf_flag = False

    # Open Files
    inputfile = open(tplfile, 'r')

    for l in inputfile:
        j += 1
        # if j == 1232:
        #     print("Stop")
        if dutflow_pa.search(l):
            dutflow = dutflow_pa.search(l).group(1)
            dutf_flag = True
            dutfi = {}
        if dutflowitem_pa.search(l) and dutf_flag:
            dutflowitem = dutflowitem_pa.search(l).group(1)
        if port_pa.search(l) and dutf_flag:
            port_no = port_pa.search(l).group(1)
            setctr = False
            setbin = False
        if pf_pa.search(l) and dutf_flag:
            pf = pf_pa.search(l).group(1)
        if counter_pa.search(l) and dutf_flag:
            setctr = True
        if bin_pa.search(l) and dutf_flag:
            setbin = True
        if (goto_pa.search(l) or return_pa.search(l)) and dutf_flag:
            if goto_pa.search(l):
                results = goto_pa.search(l).group(1)
            elif return_pa.search(l):
                results = return_pa.search(l).group(1)
            if dutflowitem in dutfi.keys():
                dutfi[dutflowitem].update({port_no:
                                           (pf, setctr, setbin, results)})
            else:
                dutfi[dutflowitem] = {port_no:
                                      (pf, setctr, setbin, results)}
        if dutf_flag and r_brace_pa.search(l):
            dutf[dutflow] = dutfi
            dutf_flag = False

    return dutf


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print("Must Specify TP Path! For example: ")
        print("+------------------------------------------------------------+")
        print("| tpl_tools TP_PATH\TPL\                                     |")
        print("+------------------------------------------------------------+")
        sys.exit(0)

    TPPath = sys.argv[-1]
    print("\nYou are using TP: ", TPPath, '\n')

    tpl_list = getTPLList(TPPath)
    # ipdb.set_trace()

    m = 0
    t = 0
    Modules = []
    modulename = ''
    for tpl in tpl_list:
        # print(tpl)
        t += 1
        module = tpl.split("\\")[-2]
        if module in ignore_MO_list:
            if modulename != module:
                print("-" * 10 + "Pay attention: Module \"" +
                      module + "\" is in module ignore list!")
                modulename = module
            continue
        else:
            if isfile(tpl + '.old'):
                print("Original tpl file has already backuped.\n")
                rename(tpl + '.old', tpl + '.org')
                if isfile(tpl):
                    rename(tpl, tpl + '.old')
            else:
                rename(tpl, tpl + '.old')

            if module not in Modules:
                Modules.append(module)
                m += 1
                print(str(m) + ". Now work with module: " + module)
                t = 1
            print("\t" + str(t) + "). Processing", tpl)
            dutdict = parseTPL(tpl + '.old')
            tplmodify(tpl + '.old', tpl, module, dutdict)
