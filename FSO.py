from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QFileDialog
import sys
import os
import icons
from subprocess import Popen
from analyzeResults import Ui_AnalyzeResults
from scriptFunctions import launchXmippScript, launchChimeraSCript, addcolonmrc
import configparser


class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow_v0.ui', self)
        
        configFile = configparser.ConfigParser()
        configFile.read('config.ini')
        
        self.xmippPath = configFile['EXTERNAL_PROGRAMS']['XMIPP_PATH']
        self.chimeraPath = configFile['EXTERNAL_PROGRAMS']['CHIMERA_PATH']
        
        self.pathApp = os.getcwd()
        self.resultsPath = self.pathApp + "/results/"
        
        self.linePathDir.setText(self.pathApp)
        
        #Path line and path button
        self.linePathDir = self.findChild(QtWidgets.QLineEdit, 'linePathDir')
        self.pathButton = self.findChild(QtWidgets.QPushButton, 'pathButton')
        self.pathButton.clicked.connect(self.browsePath)
        
        #Lab website button
        self.YaleButton = self.findChild(QtWidgets.QPushButton, 'YaleButton')
        self.YaleButton.clicked.connect(self.labwebsite)
        
        #Help button
        self.helpButton = self.findChild(QtWidgets.QPushButton, 'HelpButton')
        self.helpButton.clicked.connect(self.helpApp)
        
        #Cite button
        self.citeButton = self.findChild(QtWidgets.QPushButton, 'citeButton')
        self.citeButton.clicked.connect(self.cite)
        
        #Map 1
        self.browseMap1 = self.findChild(QtWidgets.QPushButton, 'browseMap1')
        self.viewMap1 = self.findChild(QtWidgets.QPushButton, 'showChimeraMap1')
        self.viewMap1.clicked.connect(lambda: self.showChimera(self.lineMap1.text()))
        self.browseMap1.clicked.connect(self.setMap1)

        #Map 2
        self.browseMap2 = self.findChild(QtWidgets.QPushButton, 'browseMap2')
        self.viewMap2 = self.findChild(QtWidgets.QPushButton, 'showChimeraMap2')
        self.viewMap2.clicked.connect(lambda: self.showChimera(self.lineMap2.text()))
        self.browseMap2.clicked.connect(self.setMap2)
        
        #Mask
        self.mask = self.findChild(QtWidgets.QPushButton, 'browseMask')
        self.viewMask = self.findChild(QtWidgets.QPushButton, 'showChimeraMask')
        self.viewMask.clicked.connect(lambda: self.showChimera(self.lineMask.text()))
        self.mask.clicked.connect(self.setMask)
        
        #Particles
        #self.particles = self.findChild(QtWidgets.QPushButton, 'browseParticles')
        #self.particles.clicked.connect(self.setParticles)
        
        #Execute Button and Analyze
        self.execute = self.findChild(QtWidgets.QPushButton, 'ExecuteButton')
        self.execute.clicked.connect(self.executeButton)
        self.analyze = self.findChild(QtWidgets.QPushButton, 'AnalyzeButton_2')
        self.analyze.clicked.connect(self.analyzeButton)
        
        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyRead.connect(self.executeButton)
        self.console = self.findChild(QtWidgets.QTextEdit, 'consoleOutput')
        
        #Checkbox bestAngle
        self.bestAngle = self.findChild(QtWidgets.QCheckBox, 'checkBox')
        self.coneAngle = self.findChild(QtWidgets.QLineEdit, 'lineCone')
        self.angleLabel = self.findChild(QtWidgets.QLabel, 'angleLabel')
        self.angleLabel.hide()
        self.coneAngle.hide()
        self.bestAngle.stateChanged.connect(self.bestAngleclick)
        # self.console.setReadOnly(True)
        
        self.show()
    
    def browsePath(self):
        self.pathApp = QFileDialog.getExistingDirectory(self,    "Set working directory", QtCore.QCoreApplication.applicationDirPath())
        self.linePathDir.setText(self.pathApp)
        self.resultsPath = self.pathApp + "/results/"
        
    def labwebsite(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://noodle.med.yale.edu/hdtag/profile.html"));

    def helpApp(self):
        QtWidgets.QMessageBox.about(self, "About the algorithm",
                       "<b>Directional Fourier Shell Correlation (FSC)</b><br>"
                       "<small>This program may be used to estimate the directional FSC between two half maps. The directionality is measured by means of conical-like filters in Fourier Space. To avoid possible Gibbs effects the filters are gaussian functions with their respective maxima along the filtering direction. A set of 321 directions is used to cover the projection sphere, computing for each direction the directional FSC at 0.143 between the two half maps. The result is a set of 321 FSC curves. From then a 3DFSC is obtained by interpolation. Note that as well as it occurs with  global FSC, the directional FSC is mask dependent.</small><br>"
                       "<br>"
                       "<b>Occupancy Fourier Shell Occupancy (FSO)</b><br>"
                       "<small>The Occupancy Fourier Shell Curve can be obtained from the set of directional FSC curves estimated before. To do that, the two half maps are used to determine the Global FSC at threshold 0.143. Then, the ratio between the number of directions with resolution higher (better) than the Global resolution and the total number of measured directions is calculated at different frequencies (resolutions). Note that this ratio is between 0 (all directions presents worse) resolution than the global FSC)  and 1 (all directions present better resolution than the FSC) at a given resolution. In the particular case for which the FSO curve takes the value of 0.5, then half of the directions are better, and the other half are worse than the FSC. Therefore, the FSO curve at 0.5 should be the FSC value. Note that a map is isotropic if all directional resolution are similar, and anisotropic is there are significant resolution values along  different directions. Thus, when the OFSC present a sharp cliff, it means step-like function the map will be isotropic. In contrast, when the FSO shows a slope the map will be anisotropic. The lesser slope the higher resolution isotropy. </small><br>"
                       "<br>"
                       "<b>Particle contribution to the resolution</b><br>"
                       "<small>If a set of particle is provided, the algorithm will determine the contribution of each particle to the directional resolution and it's effect in the resolution anisotropy. It means to determine if the directional resolution is explained by particles. If not, then probably your set of particle contains empty particles (noise), the reconstruction presents heterogeneity or flexibility, in that the heterogeneity should be solved and the map reconstructed again</small>");


    def cite(self):
        QtWidgets.QMessageBox.about(self, "Reference of the algorithm",
                                    "Reference: J.L. Vilas, H.D. Tagare, XXXXX (2020)")

    def setMap1(self):
        pathlineMap1 = QFileDialog.getOpenFileName(self,    "Select Half Map 1", self.pathApp)
        self.lineMap1.setText(pathlineMap1[0])
    
    def setMap2(self):
        pathlineMap2 = QFileDialog.getOpenFileName(self,    "Select Half Map 2", self.pathApp)
        self.lineMap2.setText(pathlineMap2[0])
    
    def setMask(self):
        pathMask = QFileDialog.getOpenFileName(self,    "Select Mask", self.pathApp)
        self.lineMask.setText(pathMask[0])
        
    def setParticles(self):
        pathParticles = QFileDialog.getOpenFileName(self,    "Select metadata Particles", self.pathApp)
        self.lineParticles.setText(pathParticles[0])
        
    def showChimera(self, fn):
        launchChimeraSCript(fn, self.chimeraPath)
    
    # def execute(cmd):
    #     proc = Popen(cmd, shell=True, stdout=PIPE, bufsize=1, universal_newlines=True)
        
    #     while True:
    #         line = proc.stdout.readline()
            
    #         if not line:
    #             break
    #         print(line, end ='')
        
    #     proc.wait()
    
    def executeButton(self):
        xmippCmdline, params = self.createXmippScript()
        
        if not os.path.exists(self.resultsPath):
            os.makedirs(self.resultsPath)
        
        xmippCmdline = xmippCmdline + " " + params
        env_var = os.environ
        os.environ['XMIPP_HOME'] = self.xmippPath
        os.environ['PATH'] = self.xmippPath +'/bin'+':'+os.environ['PATH']
        os.environ['LD_LIBRARY_PATH'] = self.xmippPath + '/lib'+':'+os.environ['LD_LIBRARY_PATH']
        
        # from subprocess import Popen, PIPE, CalledProcessError
        
        # cmd = " ".join(["python -u -m"] + xmippCmdline) 
            
            
        import subprocess
        
        process = subprocess.run([xmippCmdline], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, bufsize=1)
        print(process.stdout)
        
        self.analyze.setEnabled(True)
   
    def onUpdateText(self, text):
        cursor = self.console.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.console.setTextCursor(cursor)
        self.console.ensureCursorVisible()
     
    def analyzeButton(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_AnalyzeResults(self.chimeraPath, self.resultsPath)

    def createXmippScript(self):
        program = "xmipp_resolution_directional_FSC "
        params =  " --half1 %s" % addcolonmrc(self.lineMap1.text())
        params += " --half2 %s" % addcolonmrc(self.lineMap2.text()) 
        if (self.lineMask.text() != ""):
            params += " --mask " % (addcolonmrc(self.lineMask.text()))
        if (self.lineParticles.text() != ""):
            params += " --particles %s" % (self.lineParticles.text())
        params += " --anisotropy %s" % (self.resultsPath + "anisotropy.xmd")
        params += " --threedfsc %s"  % (self.resultsPath +"threeDfsc.mrc")
        if (self.bestAngle.isChecked() is False):
            params += " --anglecone %s" % self.coneAngle.text()
        params += " --sampling %s" % self.lineSampling.text();
        params += " --fscfolder %s" % self.resultsPath
    
        return program, params;
    
    def bestAngleclick(self):
        if (self.checkBox.isChecked()):
            self.lineCone.hide();
            self.lineCone.clear();
            self.angleLabel.hide();
        else:
            self.lineCone.show();
            self.angleLabel.show();
  
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
