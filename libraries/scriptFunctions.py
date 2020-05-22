#!../env/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:47:26 2020

@author: vilas
"""
import subprocess
import os

def addcolonmrc(fn):
    fn_slit = os.path.splitext(fn)
    if (fn_slit[-1] == ".mrc") or (fn_slit[-1] == ".map"):
        return fn+":mrc"
    else:
        return fn
    

def launchXmippScript(xmippCmdline, xmippPath):

    print(xmippCmdline)
    os.environ['XMIPP_HOME'] = xmippPath
    os.environ['PATH'] = xmippPath +'/bin:$PATH'
    os.environ['LD_LIBRARY_PATH'] = xmippPath + '/lib'
    # os.system(xmippCmdline)
    process = subprocess.Popen([xmippCmdline],
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout, stderr
    
def launchChimeraSCript(cmdScriptOrFile, chimeraPath):
    print(chimeraPath)
    pathToOpen = chimeraPath + " " + cmdScriptOrFile
    os.system(pathToOpen)
    
    


