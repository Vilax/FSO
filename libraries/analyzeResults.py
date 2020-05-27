#!../env/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:46:30 2020

@author: vilas
"""

from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QFileDialog

# import os
import icons
from libraries.plot_module import plotFSC
from libraries.plotWindow import PlotAgainstResolution, PlotAngular
from libraries.scriptFunctions import launchChimeraSCript
# from confPaths import confPaths

class Ui_AnalyzeResults(QtWidgets.QDialog):
    def __init__(self, chimeraPath, resultsPath):
        super(Ui_AnalyzeResults, self).__init__()
        uic.loadUi('GUI/analyzewindow_v0.ui', self)
        self.chimeraPath = chimeraPath
        self.resultsPath = resultsPath
        
        self.show()

        #show FSC
        self.showFSCButton = self.findChild(QtWidgets.QPushButton, 'showGlobalFSC')
        self.showFSCButton.clicked.connect(self.showFSC)
        
        #show DirectionalFSC
        self.showDirFSCButton = self.findChild(QtWidgets.QPushButton, 'showDirFSC')
        self.dirNum = self.findChild(QtWidgets.QLineEdit, 'selectDir')
        self.showDirFSCButton.clicked.connect(self.showdirectionalFSC)
        
        #show FSO
        self.showFOSButton = self.findChild(QtWidgets.QPushButton, 'showOFSC')
        self.showFOSButton.clicked.connect(self.showFOS) 
        
        #show Resolution from particles
        #self.showResParticlesButton = self.findChild(QtWidgets.QPushButton, 'showResolutionFromParticles')
        #self.showResParticlesButton.clicked.connect(self.showResParticles) 
        
        #show Resolution distribution
        self.showResDistButton = self.findChild(QtWidgets.QPushButton, 'showDirectionalResolutionDistribution')
        self.showResDistButton.clicked.connect(self.showResDistribution) 
        
        #show Particle Distribution
        #self.showPartDistButton = self.findChild(QtWidgets.QPushButton, 'showParticleDistribution')
        #self.showPartDistButton.clicked.connect(self.showParticlesDistribution) 
        
        #show 3DFSC
        self.show3DFSCButton = self.findChild(QtWidgets.QPushButton, 'show3DFSC')
        self.show3DFSCButton.clicked.connect(self.show3DFSCChimera) 
  
        #show Directional Filtered Map
        self.showDirFiltMapButton = self.findChild(QtWidgets.QPushButton, 'showFilteredMap')
        self.showDirFiltMapButton.clicked.connect(self.showDirectionalFilteredMapChimera)       
        
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

    def showdirectionalFSC(self):
        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'fscDirection_' + self.dirNum.text()+ '.xmd'
        labelX = "_resolutionFreqFourier"
        labelY = "_resolutionFRC"
        xlabel = 'Resolution (1/A)'
        ylabel = 'FSC (a.u.)'
        title = 'Directional Resolution - FSC'
        hthresholds = [0.143]
        self.ui = PlotAgainstResolution(pathFile, labelX, labelY, xlabel, ylabel, title, hthresholds)


    def showFOS(self):
        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'anisotropy.xmd'
        labelX = "_resolutionFreqFourier"
        labelY = "_resolutionFRC"
        xlabel = 'Resolution (1/A)'
        ylabel = 'FSO (a.u.)'
        title = 'Fourier Shell Occupancy - FSO'
        hthresholds = [0.1, 0.5, 0.9]
        self.ui = PlotAgainstResolution(pathFile, labelX, labelY, xlabel, ylabel, title, hthresholds)

    def showResParticles(self):
        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'ParticlesDist_and_Contribution.xmd'
        labelRadial = "_angleTilt"
        labelAzimutal = "_angleRot"
        labelCounts = "_weight"
        xlabel = None
        ylabel = None
        title = 'Resolution distribution from particles (prediction)'
        self.ui = PlotAngular(pathFile, labelRadial, labelAzimutal, labelCounts, xlabel, ylabel, title)
 
    def showResDistribution(self):
        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'Resolution_Distribution.xmd'
        labelRadial = "_angleTilt"
        labelAzimutal = "_angleRot"
        labelCounts = "_resolutionFRC"
        xlabel = None
        ylabel = None
        title = 'Resolution Distribution'
        self.ui = PlotAngular(pathFile, labelRadial, labelAzimutal, labelCounts, xlabel, ylabel, title)
 
    def showParticlesDistribution(self):
        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'ParticlesDist_and_Contribution.xmd'
        labelRadial = "_angleTilt"
        labelAzimutal = "_angleRot"
        labelCounts = "_count"
        xlabel = None
        ylabel = None
        title = 'Particles Distribution'
        self.ui = PlotAngular(pathFile, labelRadial, labelAzimutal, labelCounts, xlabel, ylabel, title)
        
    def show3DFSCChimera(self):
        self.window = QtWidgets.QMainWindow()
        pathFile_3DFSC  = self.resultsPath + 'threeDfsc.mrc'
        pathFile_sphere = self.resultsPath + 'sphere.mrc'
        launchChimeraSCript(pathFile_3DFSC, self.chimeraPath)
 
    def showDirectionalFilteredMapChimera(self):
        path_filtMap  = self.resultsPath + 'filteredMap.mrc'
        launchChimeraSCript(path_filtMap, self.chimeraPath)
            
