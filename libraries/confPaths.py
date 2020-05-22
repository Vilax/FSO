#!../env/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:23:01 2020

@author: vilas
"""
import configparser
import os

class confPaths:
    def __init__(self):
        self.xmippPath = None
        self.chimeraPath = None
        self.resultsPath = None
        self.pathApp = None

    def loadConfigurationPaths(self):

        self.pathApp = os.getcwd() + "/config";
        
        configFile = configparser.ConfigParser()
        configFile.read('config.ini')
        
        self.xmippPath = configFile['EXTERNAL_PROGRAMS']['XMIPP_PATH']
        self.chimeraPath = configFile['EXTERNAL_PROGRAMS']['CHIMERA_PATH']
        
        # print("Please check the following paths. If any of them is empty, then open"
        #          "the config file and edit the correspondi line. This file must be located"
        #          "in the same folder than your program.")
  
