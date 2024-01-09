#!/usr/bin/env python3

# Owned
__author__ = "Giana Nicolini (INAF - OATo)"
__copyright__ = "TBD"
__credits__ = [""]
__license__ = "GPL"
__maintainer__ = "Giana Nicolini"
__email__ = "gianalfredo.nicolini@inaf.it"
__status__ = "beta"

# Change Log
# Ver       Date       Description
# --------- ---------- -----------------------------------------------
#     0.0.2 2023-10-20 Beta
__version__ = "0.0.2_20231220"

import pandas as pd
import yaml
import os
import PlatoRepo as PR

# how to share variables among classes:
#
# class Child():
#   def __init__(self):
#     self.var_2 = "World"
#
# class Main():
#   def __init__(self):
#     self.var_1 = "Hello"
#     self.child = Child()
#     print("Inside class:", self.var_1, self.child.var_2)
#
# main = Main()
# print("Outside class:", main.var_1, main.child.var_2)

# How to share variables among methods:
#
# class TestClass(object):
#
#     def __init__(self):
#         self.test = None
#
#     def current(self, test):
#         """Just a method to get a value"""
#         self.test = test
#         print(test)
#
#     def next_one(self):
#         """Trying to get a value from the 'current' method"""
#         new_val = self.test
#         print(new_val)

        

# read the configuration file
with open('CAM-2046.yaml', 'r') as file:
    cfg = yaml.safe_load(file)
repoRoot =  cfg['ArchiveRoot']
T0 = cfg['TimeStart']
T1 = cfg['TimeEnd']
parameters = cfg['Parameters']
obsId = cfg['OBSID']
camId = cfg['CamID']
ComplRange = cfg['ComplRange']
TRP1_123 = []
IAS_HK = PR.HK(repoRoot)
IAS_HK.load(camId)
for HKParam in parameters:
    # Seleziona TRP1-1, TRP1-2 e TRP1-3
    PP = IAS_HK.Param(HKParam)
    # Seleziona OBSID
    PPV = PP.getValuesByOBSID(obsid=obsId)
    # print(PPV)
    # compute the average over the OBSID
    TRP1_123.append(PPV['Values'].mean())
    # PPV = PP.getValuesByTime(T0=T0, T1=T1, OOLL=-79.1400, OOLH=-79.1370)
print(TRP1_123)
a = [1, 0, 1, 0, 1, 0, 1]
b = [0, 1, 1, 0, 0, 1, 1]
c = [0, 0, 0, 1, 1, 1, 1]

out = 'TRP1-1 [°C],TRP1-2 [°C],TRP1-3 [°C],Mean [°C],Range [°C],OK/NOK\n'
rangeT = '[' + str(ComplRange[0]) + ' ; ' + str(ComplRange[1]) + ']'
for idx in range(7):
    mean = (a[idx]*TRP1_123[0] + b[idx]*TRP1_123[1] + c[idx]*TRP1_123[2]) / (a[idx] + b[idx] + c[idx])
    TRP11T = '--'
    TRP12T = '--'
    TRP13T = '--'
    if a[idx] == 1:
        TRP11T = f'{TRP1_123[0]:.2f}'
    if b[idx] == 1:
        TRP12T = f'{TRP1_123[1]:.2f}'
    if c[idx] == 1:
        TRP13T = f'{TRP1_123[2]:.2f}'
    if mean <= ComplRange[0] and mean >= ComplRange[1]:
        compl = 'OK'
    else:
        compl = 'NOT OK'

    out = out + TRP11T + ',' + TRP12T + ',' + TRP13T + ',' + f'{mean:.2f}' + ',' + rangeT + ',' + compl + '\n'
print(out)
outf = open('CAM-2046_' + camId + '.csv', 'w')
outf.write(out)
outf.close()

    
# build the table with all 7 combinations and verify the mean is between -70 and -90
     