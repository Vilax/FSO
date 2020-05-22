#!../env/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 11:22:57 2019

# @author: jlvilas
"""

#import numpy as np
#from pyworkflow.em import ImageHandler
import matplotlib.pyplot as plt
import numpy as np
import csv
#from matplotlib import cm
#import matplotlib.colors as mcolors
#from os.path import abspath, exists

def readMetaData(metadataFile):
    file = open(metadataFile, "r")
    lines = file.readlines()
    file.close()

    labels = []
    x = []
    y = []
    print(lines[0])
    md = []
    for line in lines:
        line = line.strip()
        if line[0] == "#":
            continue
        else:
            if str.isalpha(line[0]) is True:
                continue
            else:
                if line[0] == "_":
                    labels.append(line)
                else:
                    md.append(np.fromstring(line, dtype=np.float, sep=' '))
    md = np.stack(md, axis=0)

    md = md.transpose()
    mdDict = dict(zip(labels, md))

    return mdDict


def formatFreq(value, pos):
    """ Format function for Matplotlib formatter. """
    inv = 999.
    if value:
        inv = 1 / value
    return "1/%0.2f" % inv


def plotFSC(metadataFile, labelX, labelY, xlabel, ylabel, title):
    mdDict = readMetaData(metadataFile)
    x = mdDict[labelX]
    y = mdDict[labelY]
    fig, ax = plt.subplots()
    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(formatFreq))
    ax.set_ylim([-0.1, 1.1])
    ax.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.hlines(0.143, x[0], x[-1], colors = 'k', linestyles = 'dashed')
    plt.grid(True)
    plt.show()


def plotFOS(metadataFile, labelX, labelY, xlabel, ylabel, title):
    mdDict = readMetaData(metadataFile)

    x = mdDict[labelX]
    y = mdDict[labelY]
    fig, ax = plt.subplots()

    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(formatFreq))
    ax.set_ylim([-0.1, 1.1])
    ax.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.hlines(0.1, x[0], x[-1], colors = 'k', linestyles = 'dashed')
    plt.hlines(0.5, x[0], x[-1], colors='k', linestyles='dashed')
    plt.hlines(0.9, x[0], x[-1], colors='k', linestyles='dashed')
    plt.grid(True)
    plt.show(block=False)
    plt.show()


def plotXY(metadataFile, labelX, labelY, xlabel, ylabel, title):
    mdDict = readMetaData(metadataFile)

    x = mdDict[labelX]
    y = mdDict[labelY]
    fig, ax = plt.subplots()

    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(formatFreq))

    ax.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show(block=False)
    plt.show()

def plotParticleDistribution(metadataFile, labelRadial, labelAzimutal, labelCounts, xlabel, ylabel, title):
    plotPolar(metadataFile, labelRadial, labelAzimutal, labelCounts, xlabel, ylabel, title, True)

# def plotPolar(metadataFile, labelRadial, labelAzimutal, labelCounts, xlabel, ylabel, title, preprocess = False):
#     mdDict = readMetaData(metadataFile)

#     radius = mdDict[labelRadial]
#     azimuth = mdDict[labelAzimutal]
#     counts = mdDict[labelCounts]

#     # Detect the coordinate system
#     rmin = np.amin(azimuth)
#     rmax = np.amax(azimuth)
#     tmin = np.amin(radius)
#     tmax = np.amax(radius)

#     if (rmin < -90) or (tmax < 90):
#         print('The angular assigment does not follow the criterion of'
#               'rot in [0,360) and tilt in [0,90]. The angles will be '
#               'be converted into this criterion.')
#         print('The detected criterion consider a rot in [-180,180) and '
#               ' a tilt in [0,90]. The angles will be converted into '
#               ' rot in [0,360) and tilt in [0,90]. If the result is not'
#               ' correct please check that the input set of particles has'
#               ' the angles following this criterion rot in [0,360) and '
#               ' tilt in [0,90]')
#         idx = azimuth < 0
#         azimuth[idx] = azimuth[idx] + 360

#     if ((rmin < 0) and (rmin > -90)) or (tmax > 90):
#         print('The angular assigment does not follow the criterion of'
#               'rot in [0,360) and tilt in [0,90]. The angles will be '
#               'be converted into this criterion.')
#         print('The detected criterion consider a rot in [-90,90) and '
#               ' a tilt in [0,180]. The angles will be converted into '
#               ' rot in [0,360) and tilt in [0,90]. If the result is not'
#               ' correct please check that the input set of particles has'
#               ' the angles following this criterion rot in [0,360) and '
#               ' tilt in [0,90]')

#         for k in np.arange(0, len(azimuth)):
#             if (azimuth[k] < 0) and (azimuth[k] <= 90):
#                 azimuth[k] = azimuth[k] + 360
#             else:
#                 if (azimuth[k] < 0) and (azimuth[k] > 90):
#                     azimuth[k] = azimuth[k] + 180
#                     radius[k] = 180 - radius[k]
#                 else:
#                     if (azimuth[k] >= 0) and (radius[k] > 90):
#                         azimuth[k] = azimuth[k] + 180;
#                         radius[k] = 180 - radius[k];

#     # define binning
#     azimuths = np.radians(np.linspace(0, 360, 360))
#     zeniths = np.arange(0, 91, 1)

#     r, theta = np.meshgrid(zeniths, azimuths)

#     values = np.zeros((len(azimuths), len(zeniths)))

#     if preprocess is False:
#         for i in np.arange(0, len(azimuth)):
#             values[int(azimuth[i]), int(radius[i])] = counts[i]
#     else:
#         for i in np.arange(0, len(azimuth)):
#             values[int(azimuth[i]), int(radius[i])] += 1

#     # ------ Plot ------
#     fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
#     pc = ax.contourf(theta, r, values, np.arange(0, values.max(), .1))

#     fig.colorbar(pc)
#     plt.title(title)

#     return plt.show()

# def plotPolar(metadataFile, labelRadial, labelAzimutal, labelCounts, xlabel, ylabel, title, preprocess = False):
#     mdDict = readMetaData(metadataFile)

#     radius = mdDict[labelRadial]
#     azimuth = mdDict[labelAzimutal]
#     counts = mdDict[labelCounts]

#     # Detect the coordinate system
#     rmin = np.amin(azimuth)
#     rmax = np.amax(azimuth)
#     tmin = np.amin(radius)
#     tmax = np.amax(radius)

#     if (rmin < -90) or (tmax < 90):
#         print('The angular assigment does not follow the criterion of'
#               'rot in [0,360) and tilt in [0,90]. The angles will be '
#               'be converted into this criterion.')
#         print('The detected criterion consider a rot in [-180,180) and '
#               ' a tilt in [0,90]. The angles will be converted into '
#               ' rot in [0,360) and tilt in [0,90]. If the result is not'
#               ' correct please check that the input set of particles has'
#               ' the angles following this criterion rot in [0,360) and '
#               ' tilt in [0,90]')
#         idx = azimuth < 0
#         azimuth[idx] = azimuth[idx] + 360

#     if ((rmin < 0) and (rmin > -90)) or (tmax > 90):
#         print('The angular assigment does not follow the criterion of'
#               'rot in [0,360) and tilt in [0,90]. The angles will be '
#               'be converted into this criterion.')
#         print('The detected criterion consider a rot in [-90,90) and '
#               ' a tilt in [0,180]. The angles will be converted into '
#               ' rot in [0,360) and tilt in [0,90]. If the result is not'
#               ' correct please check that the input set of particles has'
#               ' the angles following this criterion rot in [0,360) and '
#               ' tilt in [0,90]')

#         for k in np.arange(0, len(azimuth)):
#             if (azimuth[k] < 0) and (azimuth[k] <= 90):
#                 azimuth[k] = azimuth[k] + 360
#             else:
#                 if (azimuth[k] < 0) and (azimuth[k] > 90):
#                     azimuth[k] = azimuth[k] + 180
#                     radius[k] = 180 - radius[k]
#                 else:
#                     if (azimuth[k] >= 0) and (radius[k] > 90):
#                         azimuth[k] = azimuth[k] + 180;
#                         radius[k] = 180 - radius[k];

#     # define binning
#     azimuths = np.radians(np.linspace(0, 360, 360))
#     zeniths = np.arange(0, 91, 1)

#     r, theta = np.meshgrid(zeniths, azimuths)

#     values = np.zeros((len(azimuths), len(zeniths)))

#     if preprocess is False:
#         for i in np.arange(0, len(azimuth)):
#             values[int(azimuth[i]), int(radius[i])] = counts[i]
#     else:
#         for i in np.arange(0, len(azimuth)):
#             values[int(azimuth[i]), int(radius[i])] += 1

#     # ------ Plot ------
#     fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
#     pc = ax.contourf(theta, r, values, np.arange(0, values.max(), .1))

#     fig.colorbar(pc)
#     plt.title(title)

#     return plt.show()


"""

@staticmethod
def getColorMapChoices():
    return plt.colormaps()

def _showOriginalVolumeSlices(self, param=None):
    cm = DataView(self.protocol.half1.get().getFileName())
    cm2 = DataView(self.protocol.half2.get().getFileName())
    return [cm, cm2]

def _show3DFSC(self, param=None):
    cm = DataView(self.protocol._getExtraPath(OUTPUT_3DFSC))
    return [cm]





def _show3DFSCcolorSlices(self, param=None):
    self._showColorSlices(OUTPUT_3DFSC, 1, '3DFSC Color Slices', 1, 1)

def _showChimera3DFSC(self, param=None):
    fnmap = abspath(self.protocol._getFileName(OUTPUT_3DFSC))  # 'extra/'+
    fnsphere = abspath(self.protocol._getFileName(OUTPUT_SPHERE))  # 'extra/fsc/'
    self.createChimeraScript(fnmap, fnsphere)
    cmdFile = self.protocol._getExtraPath('chimeraVisualization.cmd')
    view = ChimeraView(cmdFile)
    return [view]

def _showDirectionalFSCCurve(self, paramName=None):
    fnmd = self.protocol._getExtraPath('fsc/' + 'fscDirection_%i.xmd' % self.fscNumber.get())
    title = 'Directional FSC'
    xTitle = 'Resolution (1/A)'
    yTitle = 'FSC (a.u.)'
    mdLabelX = xmippLib.MDL_RESOLUTION_FREQ
    mdLabelY = xmippLib.MDL_RESOLUTION_FRC
    self._plotCurveFSC(fnmd, title, xTitle, yTitle, mdLabelX, mdLabelY)

def _showAnisotropyCurve(self, paramName=None):
    fnmd = self.protocol._getExtraPath('anisotropy.xmd')
    title = 'Anisotropy Curve'
    xTitle = 'Resolution (1/A)'
    yTitle = 'Anisotropy (a.u.)'
    mdLabelX = xmippLib.MDL_RESOLUTION_FREQ
    mdLabelY = xmippLib.MDL_RESOLUTION_FRC
    self._plotCurveAnisotropy(fnmd, title, xTitle, yTitle, mdLabelX, mdLabelY)

def _showDirectionalFilter(self, param=None):
    cm = DataView(self.protocol._getExtraPath(OUTPUT_DIRECTIONAL_FILTER))
    cm2 = DataView(self.protocol.half1.get().getFileName())
    return [cm, cm2]

def _showOneColorslice(self, param=None):
    img = ImageHandler().read(self.protocol._getExtraPath(OUTPUT_3DFSC))
    imgData = img.getData()
    # imgData2 = np.ma.masked_where(imgData < 0.001, imgData, copy=True)
    max_Res = np.nanmax(imgData)
    min_Res = np.nanmin(imgData)
    # imageFile = self.protocol._getExtraPath(OUTPUT_3DFSC)
    # imgData, min_Res, max_Res = self.getImgData(imageFile)

    xplotter = XmippPlotter(x=1, y=1, mainTitle="3DFSC Slices "
                                                "along %s-axis."
                                                % self._getAxis())
    sliceNumber = self.sliceNumber.get()
    if sliceNumber < 0:
        x, _, _, _ = ImageHandler().getDimensions(imageFile)
        sliceNumber = x / 2
    else:
        sliceNumber -= 1
    # sliceNumber has no sense to start in zero
    a = xplotter.createSubPlot("Slice %s" % (sliceNumber + 1), '', '')
    matrix = self.getSliceImage(imgData, sliceNumber, self._getAxis())
    plot = xplotter.plotMatrix(a, matrix, min_Res, max_Res,
                               cmap=self.getColorMap(),
                               interpolation="nearest")
    xplotter.getColorBar(plot)

    return [plt.show(xplotter)]
"""

#def _formatFreq(self, value, pos):
#    """ Format function for Matplotlib formatter. """
#    inv = 999.
#    if value:
#        inv = 1 / value
#    return "1/%0.2f" % inv
"""
def _plotCurveFSC(self, fnmd, title, xTitle, yTitle, mdLabelX, mdLabelY):
    md = xmippLib.MetaData(fnmd)
    xplotter = XmippPlotter(figure=None)
    xplotter.plot_title_fontsize = 11

    a = xplotter.createSubPlot(title, xTitle, yTitle, 1, 1)
    xplotter.plotMdFile(md, mdLabelX, mdLabelY, 'g')
    from matplotlib.ticker import FuncFormatter
    from matplotlib.pyplot import hlines
    a.xaxis.set_major_formatter(FuncFormatter(self._formatFreq))
    xx, yy = self._prepareDataForPlot(md, mdLabelX, mdLabelY)
    a.hlines(0.143, xx[0], xx[-1], colors='k', linestyles='dashed')
    a.grid(True)

    return plt.show(xplotter)

def _plotCurveAnisotropy(self, fnmd, title, xTitle, yTitle, mdLabelX, mdLabelY):
    md = xmippLib.MetaData(fnmd)
    xplotter = XmippPlotter(figure=None)
    xplotter.plot_title_fontsize = 11

    a = xplotter.createSubPlot(title, xTitle, yTitle, 1, 1)
    xplotter.plotMdFile(md, mdLabelX, mdLabelY, 'g')
    from matplotlib.ticker import FuncFormatter
    from matplotlib.pyplot import hlines
    a.xaxis.set_major_formatter(FuncFormatter(self._formatFreq))
    xx, yy = self._prepareDataForPlot(md, mdLabelX, mdLabelY)
    a.hlines(0.9, xx[0], xx[-1], colors='k', linestyles='dashed')
    a.hlines(0.5, xx[0], xx[-1], colors='k', linestyles='dashed')
    a.hlines(0.1, xx[0], xx[-1], colors='k', linestyles='dashed')
    a.grid(True)

    return plt.show(xplotter)

def _prepareDataForPlot(self, md, mdLabelX, mdLabelY):

    if mdLabelX:
        xx = []
    else:
        xx = range(1, md.size() + 1)
    yy = []
    for objId in md:
        if mdLabelX:
            xx.append(md.getValue(mdLabelX, objId))
        yy.append(md.getValue(mdLabelY, objId))
    return xx, yy

def _showParticleDistribution(self, param=None):
    fnmd = self.protocol._getExtraPath('images.xmd')
    titleName = 'Particles distribution'
    self._showPolarPlot(fnmd, titleName, True)

def _showResolutionContribution(self, param=None):
    fnmd = self.protocol._getExtraPath('fsc/Particles2ResDistribution.xmd')
    titleName = 'Contribution to resolution from particles'
    self._showPolarPlot(fnmd, titleName, False)

def _showDirectionalResolution(self, param=None):
    fnmd = self.protocol._getExtraPath('fsc/PolarResolution.xmd')
    titleName = 'Directional FSC distribution'
    self._showPolarPlot(fnmd, titleName, False)

def _showPolarPlot(self, fnmd, titleName, preprocess):
    md = xmippLib.MetaData(fnmd)

    rot = []
    tilt = []
    counts = []

    for objId in md:
        rot.append(md.getValue(xmippLib.MDL_ANGLE_ROT, objId))
        tilt.append(md.getValue(xmippLib.MDL_ANGLE_TILT, objId))
        counts.append(md.getValue(xmippLib.MDL_COUNT, objId))

    rot = np.asarray(rot)
    tilt = np.asarray(tilt)
    counts = np.asarray(counts)

    # Detect the coordinate system
    rmin = np.amin(rot)
    rmax = np.amax(rot)
    tmin = np.amin(tilt)
    tmax = np.amax(tilt)

    if ((rmin < -90) or (tmax < 90)):
        print('The angular assigment does not follow the criterion of'
              'rot in [0,360) and tilt in [0,90]. The angles will be '
              'be converted into this criterion.')
        print('The detected criterion consider a rot in [-180,180) and '
              ' a tilt in [0,90]. The angles will be converted into '
              ' rot in [0,360) and tilt in [0,90]. If the result is not'
              ' correct please check that the input set of particles has'
              ' the angles following this criterion rot in [0,360) and '
              ' tilt in [0,90]')
        idx = rot < 0
        rot[idx] = rot[idx] + 360

    if (((rmin < 0) and (rmin > -90)) or (tmax > 90)):
        print('The angular assigment does not follow the criterion of'
              'rot in [0,360) and tilt in [0,90]. The angles will be '
              'be converted into this criterion.')
        print('The detected criterion consider a rot in [-90,90) and '
              ' a tilt in [0,180]. The angles will be converted into '
              ' rot in [0,360) and tilt in [0,90]. If the result is not'
              ' correct please check that the input set of particles has'
              ' the angles following this criterion rot in [0,360) and '
              ' tilt in [0,90]')

        for k in np.arange(0, len(rot)):
            if ((rot[k] < 0) and (tilt[k] <= 90)):
                rot[k] = rot[k] + 360
            else:
                if ((rot[k] < 0) and (tilt[k] > 90)):
                    rot[k] = rot[k] + 180
                    tilt[k] = 180 - tilt[k]
                else:
                    if ((rot[k] >= 0) and (tilt[k] > 90)):
                        rot[k] = rot[k] + 180;
                        tilt[k] = 180 - tilt[k];

    # define binning
    azimuths = np.radians(np.linspace(0, 360, 360))
    zeniths = np.arange(0, 91, 1)

    r, theta = np.meshgrid(zeniths, azimuths)

    values = np.zeros((len(azimuths), len(zeniths)))

    if (preprocess is False):
        for i in np.arange(0, len(rot)):
            values[int(rot[i]), int(tilt[i])] = counts[i]
    else:
        for i in np.arange(0, len(rot)):
            values[int(rot[i]), int(tilt[i])] += 1

    # values = np.random.random((azimuths.size, zeniths.size))

    # ------ Plot ------
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    pc = ax.contourf(theta, r, values, np.arange(0, values.max(), .1))

    fig.colorbar(pc)
    plt.title(titleName)

    return plt.show()

def _showColorSlices(self, fileName, setrangelimits, titleFigure, lowlim, highlim):

    img = ImageHandler().read(self.protocol._getExtraPath(fileName))
    imgData = img.getData()
    # imgData2 = np.ma.masked_where(imgData < 0.001, imgData, copy=True)
    max_Res = np.nanmax(imgData)
    min_Res = np.nanmin(imgData)
    fig, im = self._plotVolumeSlices(titleFigure, imgData,
                                     min_Res, max_Res, self.getColorMap(), dataAxis=self._getAxis())
    cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    cbar = fig.colorbar(im, cax=cax)
    cbar.ax.invert_yaxis()

    return plt.show(fig)

def _createAngDist2D(self, path):
    view = XmippPlotter(x=1, y=1, mainTitle="Highest Resolution per Direction", windowTitle="Angular distribution")
    return view.plotAngularDistributionFromMd(path, 'directional resolution distribution', min_w=0)

def _getAxis(self):
    return self.getEnumText('sliceAxis')

def _plotVolumeSlices(self, title, volumeData, vminData, vmaxData, cmap, **kwargs):
    # Get some customization parameters, by providing with default values
    titleFontSize = kwargs.get('titleFontSize', 14)
    titleColor = kwargs.get('titleColor', '#104E8B')
    sliceFontSize = kwargs.get('sliceFontSize', 10)
    sliceColor = kwargs.get('sliceColor', '#104E8B')
    size = kwargs.get('n', volumeData.shape[0])
    origSize = kwargs.get('orig_n', size)
    dataAxis = kwargs.get('dataAxis', 'z')

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    f.suptitle(title, fontsize=titleFontSize, color=titleColor, fontweight='bold')

    def getSlice(slice):
        if dataAxis == 'y':
            return volumeData[:, slice, :]
        elif dataAxis == 'x':
            return volumeData[:, :, slice]
        else:
            return volumeData[slice, :, :]

    def showSlice(ax, index):
        sliceTitle = 'Slice %s' % int(index * size / 9)
        slice = int(index * origSize / 9)
        ax.set_title(sliceTitle, fontsize=sliceFontSize, color=sliceColor)
        return ax.imshow(getSlice(slice), vmin=vminData, vmax=vmaxData,
                         cmap=self.getColorMap(), interpolation="nearest")

    im = showSlice(ax1, 3)
    showSlice(ax2, 4)
    showSlice(ax3, 5)
    showSlice(ax4, 6)

    return f, im

def _showChimera(self, param=None):
    self.createChimeraScript(OUTPUT_DOA_FILE_CHIMERA, CHIMERA_CMD_DOA, CHIMERA_ELLIP)
    cmdFile = self.protocol._getPath('chimera_DoA.cmd')
    view = ChimeraView(cmdFile)
    return [view]

def numberOfColors(self, min_Res, max_Res, numberOfColors):
    inter = (max_Res - min_Res) / (numberOfColors - 1)
    colors_labels = ()
    for step in range(0, numberOfColors):
        colors_labels += round(min_Res + step * inter, 2),
    return colors_labels

def createChimeraScript(self, map1, map2):
    scriptFile = self.protocol._getExtraPath('chimeraVisualization.cmd')
    fhCmd = open(scriptFile, 'w')
    min_Val = 0.0
    max_Val = 1.0

    numberOfColors = 21
    colors_labels = self.numberOfColors(min_Val, max_Val, numberOfColors)
    colorList = self.colorMapToColorList(colors_labels, self.getColorMap())

    fhCmd.write("open %s\n" % map1)
    fhCmd.write("open %s\n" % map2)

    smprt = self.protocol.half1.get().getSamplingRate()
    fhCmd.write("volume #0 voxelSize %s\n" % (str(smprt)))
    fhCmd.write("volume #1 voxelSize %s\n" % (str(smprt)))
    fhCmd.write("volume #1 style mesh\n")
    fhCmd.write("vol #1 hide\n")

    scolorStr = '%s,%s:' * numberOfColors
    scolorStr = scolorStr[:-1]

    line = ("scolor #0 volume #0 perPixel false cmap " + scolorStr + "\n") % colorList
    fhCmd.write(line)

    scolorStr = '%s %s ' * numberOfColors
    str_colors = ()
    for idx, elem in enumerate(colorList):
        if (idx % 2 == 0):
            if ((idx % 8) == 0):
                str_colors += str(elem),
            else:
                str_colors += '" "',
        else:
            str_colors += elem,

    line = ("colorkey 0.01,0.05 0.02,0.95 " + scolorStr + "\n") % str_colors
    fhCmd.write(line)

    fhCmd.close()

@staticmethod
def colorMapToColorList(steps, colorMap):

    # Get the map used by monoRes
    colors = ()
    ratio = 255.0 / (len(steps) - 1)
    for index, step in enumerate(steps):
        colorPosition = int(round(index * ratio))
        rgb = colorMap(colorPosition)[:3]
        colors += step,
        rgbColor = mcolors.rgb2hex(rgb)
        colors += rgbColor,

    return colors

def getColorMap(self):
    if (COLOR_CHOICES[self.colorMap.get()] is 'other'):
        cmap = cm.get_cmap(self.otherColorMap.get())
    else:
        cmap = cm.get_cmap(COLOR_CHOICES[self.colorMap.get()])
    if cmap is None:
        cmap = cm.jet
    return cmap
"""
