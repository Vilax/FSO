#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:46:30 2020

@author: vilas
"""

from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QFileDialog

# import os
import icons
from plot_module import plotFSC
from plotWindow import PlotAgainstResolution, PlotAngular
# from confPaths import confPaths

class Ui_AnalyzeResults(QtWidgets.QDialog):
    def __init__(self, chimeraPath, resultsPath):
        super(Ui_AnalyzeResults, self).__init__()
        uic.loadUi('analyzewindow.ui', self)
        self.chimeraPath = chimeraPath
        self.resultsPath = resultsPath
        
        self.show()

        #show FSC
        self.showFSCButton = self.findChild(QtWidgets.QPushButton, 'showGlobalFSC')
        self.showFSCButton.clicked.connect(self.showFSC)
        
        #show FSC
        self.showFOSButton = self.findChild(QtWidgets.QPushButton, 'showOFSC')
        self.showFOSButton.clicked.connect(self.showFOS) 
        
        #show Resolution from particles
        self.showResParticlesButton = self.findChild(QtWidgets.QPushButton, 'showResolutionFromParticles')
        self.showResParticlesButton.clicked.connect(self.showResParticles) 
        
        
        
    def showFSC(self):
        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'GlobalFSC.xmd'
        labelX = "_resolutionFreqFourier"
        labelY = "_resolutionFRC"
        xlabel = 'Resolution (1/A)'
        ylabel = 'FSC (a.u.)'
        title = 'Global Resolution - FSC'
        hthresholds = [0.143]
        self.ui = PlotAgainstResolution(pathFile, labelX, labelY, xlabel, ylabel, title, hthresholds)


    def showFOS(self):
        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'anisotropy.xmd'
        labelX = "_resolutionFreqFourier"
        labelY = "_resolutionFRC"
        xlabel = 'Resolution (1/A)'
        ylabel = 'FOS (a.u.)'
        title = 'Fourier Occupancy Shell Curve - FOS'
        hthresholds = [0.1, 0.5, 0.9]
        self.ui = PlotAgainstResolution(pathFile, labelX, labelY, xlabel, ylabel, title, hthresholds)

    def showResParticles(self):
        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'Particles2Resolution2.xmd'
        labelRadial = "_angleTilt"
        labelAzimutal = "_angleRot"
        labelCounts = "_weight"
        xlabel = None
        ylabel = None
        title = 'Resolution distribution from particles'
        preprocess = False
        self.ui = PlotAngular(pathFile, labelRadial, labelAzimutal, labelCounts, xlabel, ylabel, title, preprocess)
 
 
 
