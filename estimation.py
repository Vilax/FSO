#!./env/bin/python3
import mrcfile
import numpy as np
import directions
import sys
import os
# import icons
from subprocess import Popen
from libraries.analyzeResults import Ui_AnalyzeResults
from libraries.scriptFunctions import launchXmippScript, launchChimeraSCript, addcolonmrc
import configparser
from libraries import icons
import matplotlib.pyplot as plt


def prepareData(fnHalf1, fnHalf2, fnMask=None):
    # import matplotlib.pyplot as plt
    half1 = mrcfile.open(fnHalf1).data
    half2 = mrcfile.open(fnHalf2).data

    mask = None
    if fnMask:
        mask = mrcfile.open(fnMask).data
        half1 = np.multiply(half1, mask)
        half2 = np.multiply(half2, mask)

    # plt.imshow(half2[:,:,128])
    # plt.show()

    return half1, half2, mask


def defineFrequencies(mapSize):
    freq = np.fft.fftfreq(mapSize)
    fx, fy, fz = np.meshgrid(freq, freq, freq)

    freqMap = np.sqrt(np.multiply(fx, fx) + np.multiply(fy, fy) + np.multiply(fz, fz))

    # plt.imshow(freqMap[0, :, :])
    # plt.show()

    candidates = freqMap <= 0.5

    '''
    freqElems = np.zeros(mapSize)
    
    idx = []
    for i in range(0, candidatesIdx.size):
        j = int(candidatesIdx[i])
        idx.append(j)
        freqElems[j]+=1
    '''

    return freqMap, candidates, fx[candidates], fy[candidates], fz[candidates]


def arrangeFSC_and_fscGlobal(FT1, FT2, idxFreq, mapSize, sampling, threshold):
    Nfreqs = round(mapSize / 2)
    num = np.real(np.multiply(FT1, np.conjugate(FT2)))

    den1 = np.absolute(FT1) ** 2  # np.multiply(absz1, absz1)
    den2 = np.absolute(FT2) ** 2  # np.multiply(absz2, absz2)

    num_dirfsc = np.zeros(Nfreqs)
    den1_dirfsc = np.zeros(Nfreqs)
    den2_dirfsc = np.zeros(Nfreqs)

    fourierIdx = np.arange(0, Nfreqs)
    for i in fourierIdx:
        auxIdx = (idxFreq == i)
        num_aux = num[auxIdx]
        den1_aux = den1[auxIdx]
        den2_aux = den2[auxIdx]
        num_dirfsc[i] = np.sum(num_aux)
        den1_dirfsc[i] = np.sum(den1_aux)
        den2_dirfsc[i] = np.sum(den2_aux)

    fscglob = np.divide(num_dirfsc, np.sqrt(np.multiply(den1_dirfsc, den2_dirfsc) + 1e-38))
    fscglob[0] = 1
    digFreq = np.divide(fourierIdx + 1.0, mapSize)
    print('--> %f', sampling)
    resolutions = np.divide(sampling, digFreq)

    fig, ax = plt.subplots()
    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(formatFreq))
    ax.set_ylim([-0.1, 1.1])
    ax.plot(digFreq/sampling, fscglob)
    plt.xlabel('Resolution ($A^{-1}$)')
    plt.ylabel('FSC (a.u)')
    plt.title('FSC curve')
    hthresholds = [threshold]
    plt.hlines(hthresholds, digFreq[0], digFreq[-1], colors='k', linestyles='dashed')
    plt.grid(True)

    return num, den1, den2, fscglob, resolutions


def dirFSC(dir, ang_con, idxFreq, num, den1, den2, u, ux, uy, uz, Nfreqs, threshold, freqMat):
    cosAngle = np.cos(ang_con)

    tilt = dir[1]
    rot = dir[0]

    x_dir = np.sin(tilt) * np.cos(rot)
    y_dir = np.sin(tilt) * np.sin(rot)
    z_dir = np.cos(tilt)

    T = np.zeros([3, 3])
    T[0, 0] = x_dir * x_dir
    T[0, 1] = x_dir * y_dir
    T[0, 2] = x_dir * z_dir
    T[1, 0] = y_dir * x_dir
    T[1, 1] = y_dir * y_dir
    T[1, 2] = y_dir * z_dir
    T[2, 0] = z_dir * x_dir
    T[2, 1] = z_dir * y_dir
    T[2, 2] = z_dir * z_dir

    # It is multiply by 0.5 because later the weight is
    # cosine = sqrt(exp(-((cosine - 1) * (cosine - 1)) * aux));
    # thus the computation of the weight is speeded up

    aux = (4.0 / ((cosAngle - 1) * (cosAngle - 1)))

    # Computing directional resolution
    # angle between the position and the direction of the  cone
    cosine = np.absolute(np.divide(x_dir * ux + y_dir * uy + z_dir * uz, u + 1e-38))

    coneCandidates = cosine >= cosAngle
    cosineIdx = idxFreq[coneCandidates]

    cosine = cosine[coneCandidates]
    cosineMat = np.exp(-((cosine - 1) * (cosine - 1)) * aux)

    ##vecidx.push_back(n)
    # cosine *= cosine Commented because is equivalent to remove the root square in aux
    ##weightFSC3D.push_back(cosine);

    # selecting the frequency of the shell

    ## idxf = DIRECT_MULTIDIM_ELEM(freqidx, n)
    aux_num = np.multiply(num[coneCandidates], cosineMat)
    aux_den1 = np.multiply(den1[coneCandidates], cosineMat)
    aux_den2 = np.multiply(den2[coneCandidates], cosineMat)

    num_dirfsc = np.zeros(Nfreqs)
    den1_dirfsc = np.zeros(Nfreqs)
    den2_dirfsc = np.zeros(Nfreqs)

    # print('caca')
    # print(np.shape(aux_num))

    for i in range(0, Nfreqs):
        auxIdx = (cosineIdx == i)
        num_dirfsc[i] = np.sum(aux_num[auxIdx])
        den1_dirfsc[i] = np.sum(aux_den1[auxIdx])
        den2_dirfsc[i] = np.sum(aux_den2[auxIdx])

    fscdir = np.divide(num_dirfsc, np.sqrt(np.multiply(den1_dirfsc, den2_dirfsc)) + 1e-38)

    for i in range(len(fscdir)):
        if fscdir[i]< 0.0:
            fscdir[i] = 0.0
        if fscdir[i] >= threshold:
            freqMat[i] += T
    # idxfreqMat = fscdir>=threshold
    dirRes = 0

    return fscdir, freqMat, dirRes


def incompleteGammaFunction(x):

    idx = round(2 * x)
    if (idx > 40):
        idx = 40
    if (idx < 0):
        idx = 0

    # Table with the values of the incomplete lower gamma function. The set of values of the table can be
    # obtained in matlab with the function gammainc(x,5). The implementation of this funcitonis not easy
    # for that reason, a numerical table was put here.

    incompgamma = np.zeros(41)  # .initZeros(41);
    incompgamma[0] = 0.0
    incompgamma[1] = 0.00017212
    incompgamma[2] = 0.0036598
    incompgamma[3] = 0.018576
    incompgamma[4] = 0.052653
    incompgamma[5] = 0.10882
    incompgamma[6] = 0.18474
    incompgamma[7] = 0.27456
    incompgamma[8] = 0.37116
    incompgamma[9] = 0.4679
    incompgamma[10] = 0.55951
    incompgamma[11] = 0.64248
    incompgamma[12] = 0.71494
    incompgamma[13] = 0.77633
    incompgamma[14] = 0.82701
    incompgamma[15] = 0.86794
    incompgamma[16] = 0.90037
    incompgamma[17] = 0.92564
    incompgamma[18] = 0.94504
    incompgamma[19] = 0.95974
    incompgamma[20] = 0.97075
    incompgamma[21] = 0.97891
    incompgamma[22] = 0.9849
    incompgamma[23] = 0.98925
    incompgamma[24] = 0.9924
    incompgamma[25] = 0.99465
    incompgamma[26] = 0.99626
    incompgamma[27] = 0.9974
    incompgamma[28] = 0.99819
    incompgamma[29] = 0.99875
    incompgamma[30] = 0.99914
    incompgamma[31] = 0.99941
    incompgamma[32] = 0.9996
    incompgamma[33] = 0.99973
    incompgamma[34] = 0.99982
    incompgamma[35] = 0.99988
    incompgamma[36] = 0.99992
    incompgamma[37] = 0.99994
    incompgamma[38] = 0.99996
    incompgamma[39] = 0.99997
    incompgamma[40] = 0.99998
    val = incompgamma[idx]
    return val


def run(fnHalf1, fnHalf2, fnMask, sampling, anglecone, threshold):

    half1, half2, mask = prepareData(fnHalf1, fnHalf2, fnMask)

    FT1 = np.fft.fftn(half1)
    FT2 = np.fft.fftn(half2)
    dim = np.shape(half1)

    mapSize = dim[0]
    freqMap, candidates, fx, fy, fz = defineFrequencies(mapSize)
    idxFreq = np.round(freqMap * mapSize)  ##.astype(int)
    FT1_vec = FT1[candidates]
    FT2_vec = FT2[candidates]
    freqMap = freqMap[candidates]

    idxFreq = idxFreq[candidates]

    num, den1, den2, fscglob, resolutions = arrangeFSC_and_fscGlobal(FT1_vec, FT2_vec, idxFreq, mapSize, sampling, threshold)

    angles = directions.loadDirections()

    Ndirections = angles.shape

    ang_con = anglecone * 3.141592 / 180.0

    counter = 0
    alldirfsc = np.zeros((Ndirections[0], round(mapSize / 2)))
    freqMat = [np.zeros([3, 3]) for _ in range(round(mapSize / 2))]
    for dir in range(0, Ndirections[0]):
        counter = counter + 1
        alldirfsc[dir, :], freqMat, dirRes = dirFSC(angles[dir], ang_con, idxFreq, num, den1, den2, freqMap, fx, fy, fz,
                                                    round(mapSize / 2), threshold, freqMat)

    sig = np.copy(alldirfsc)
    sig[alldirfsc >= threshold] = 1.0
    sig[alldirfsc < threshold] = 0.0
    NdirFSCgreaterThreshold = sig.sum(axis=0)

    fso = np.divide(NdirFSCgreaterThreshold, Ndirections[0])
    fso[0] = 1
    fso[1] = 1

    binghanCurve = binghamTest(NdirFSCgreaterThreshold, freqMat, round(mapSize / 2))

    plotFSO(np.divide(sampling, resolutions)/sampling, fso, binghanCurve, 'Resolution ($A^{-1}$)', 'FSO (a.u)',
            'FSO and Bingham curves', sampling)


def binghamTest(NdirFSCgreaterThreshold, freqMat, Nfreqs):
    binghamCurve = np.zeros(Nfreqs)
    for i in range(0, Nfreqs):
        if NdirFSCgreaterThreshold[i] > 0:
            # Let us define T = 1 / n * Sum(wi * xi * xi) = > Tr(T ^ 2) = x * x + y * y + z * z
            # This is the Bingham Test (1 / 2)(p-1) * (p+2) * n * Sum(Tr(T ^ 2) - 1 / p)
            # std::cout << isotropyMatrices.at(0)[i] << aniParams.at(0)[i] << std::endl
            T = freqMat[i]/NdirFSCgreaterThreshold[i]
            T2 = np.multiply(T, T)
            trT2 = np.trace(T2)
            pdim = 3
            isotropyMatrix = 0.5 * pdim * (pdim + 2) * (2*NdirFSCgreaterThreshold[i]) * (trT2 - 1. / pdim)
            binghamCurve[i] = incompleteGammaFunction(isotropyMatrix)

    return binghamCurve


def formatFreq(value, pos):
    """ Format function for Matplotlib formatter. """
    inv = 999.
    if value:
        inv = 1 / value
    return "1/%0.2f" % inv


def interpolRes(thr, x, y):
    """
    This function is called by _showAnisotropyCurve.
    It provides the cut point of the curve defined
    by the points (x,y) with a threshold thr.
    The flag okToPlot shows if there is no intersection points
    """
    idx = np.arange(0, len(x))
    aux = np.array(y) <= thr
    idx_x = idx[aux]
    okToPlot = True
    resInterp = []
    if not idx_x.any():
        okToPlot = False
    else:
        if len(idx_x) > 1:
            idx_2 = idx_x[0]
            idx_1 = idx_2 - 1
            if idx_1 < 0:
                idx_2 = idx_x[1]
                idx_1 = idx_2 - 1
            y2 = x[idx_2]
            y1 = x[idx_1]
            x2 = y[idx_2]
            x1 = y[idx_1]
            slope = (y2 - y1) / (x2 - x1)
            ny = y2 - slope * x2
            resInterp = 1.0 / (slope * thr + ny)
        else:
            okToPlot = False

    return resInterp, okToPlot


def plotFSO(x, y1, yyBingham, xlabel, ylabel, title, sampling):
    fig, ax = plt.subplots()

    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(formatFreq))
    ax.set_ylim([-0.1, 1.1])
    ax.plot(x, y1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    hthresholds = [0.1, 0.5, 0.9]
    plt.hlines(hthresholds, x[0], x[-1], colors='k', linestyles='dashed')

    res_01, okToPlot_01 = interpolRes(0.1, x, y1)
    res_05, okToPlot_05 = interpolRes(0.5, x, y1)
    res_09, okToPlot_09 = interpolRes(0.9, x, y1)

    t = round((2 * sampling / (res_01)) * len(yyBingham)) + 3
    if t < len(yyBingham):
        for component in range(t, len(yyBingham) - 1):
            yyBingham[component] = 0
    plt.plot(x, yyBingham, 'r--')

    if (okToPlot_01 and okToPlot_05 and okToPlot_09):
        textstr = str(0.9) + ' --> ' + str("{:.2f}".format(res_09)) + 'A\n' + str(0.5) + ' --> ' + str(
            "{:.2f}".format(res_05)) + 'A\n' + str(0.1) + ' --> ' + str("{:.2f}".format(res_01)) + 'A'
        plt.axvspan(1.0 / res_09, 1.0 / res_01, alpha=0.3, color='green')

        props = dict(boxstyle='round', facecolor='white')
        plt.text(0.0, 0.0, textstr, fontsize=12, ha="left", va="bottom", bbox=props)
    plt.grid(True)
    plt.show(block=False)
    plt.show()

    '''
    def _showPolarPlot(self, fnmd):
        """
        It is called by _showDirectionalResolution
        This function shows the angular distribution of the resolution
        """
        md = emlib.MetaData(fnmd)

        radius = md.getColumnValues(emlib.MDL_ANGLE_ROT)
        azimuth = md.getColumnValues(emlib.MDL_ANGLE_TILT)
        counts = md.getColumnValues(emlib.MDL_RESOLUTION_FRC)

        # define binning
        azimuths = np.radians(np.linspace(0, 360, 360))
        zeniths = np.arange(0, 91, 1)

        r, theta = np.meshgrid(zeniths, azimuths)

        values = np.zeros((len(azimuths), len(zeniths)))

        for i in range(0, len(azimuth)):
            values[int(radius[i]), int(azimuth[i])] = counts[i]

        # ------ Plot ------
        stp = 0.1
        lowlim = max(0.0, values.min())

        highlim = values.max() + stp
        fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
        pc = plt.contourf(theta, r, values, np.arange(lowlim, highlim, stp), cmap=self.getColorMap())

        plt.colorbar(pc)
        plt.show()

    def getColorMap(self):
        cmap = cm.get_cmap(self.colorMap.get())
        if cmap is None:
            cmap = cm.jet
        return cmap

def resolutionDistribution(resDirFSC, FileName &fn)
    {
    	anglesResolution;
    	Nrot = 360
    	Ntilt = 91
    	objIdOut



    	w.initZeros(Nrot, Ntilt)
    	wt = w
    	const float cosAngle = cosf(ang_con);
    	const float aux = 4.0/((cosAngle -1)*(cosAngle -1));
    	// Directional resolution is store in a metadata
			
		for (int i=0; i<Nrot; i++)
		{
			float rotmatrix =  i*PI/180.0;
			float cr = cosf(rotmatrix);
			float sr = sinf(rotmatrix);

			for (int j=0; j<Ntilt; j++)
			{
				float tiltmatrix = j*PI/180.0;
				// position on the spehere
				float st = sinf(tiltmatrix);
				float xx = st*cr;
				float yy = st*sr;
				float zz = cosf(tiltmatrix);

				// initializing the weights
				double w = 0;
				double wt = 0;

				for (size_t k = 0; k<angles.mdimx; k++)
				{

					float rot = MAT_ELEM(angles, 0, k);
					float tilt = MAT_ELEM(angles, 1, k);

					// position of the direction on the sphere
					float x_dir = sinf(tilt)*cosf(rot);
					float y_dir = sinf(tilt)*sinf(rot);
					float z_dir = cosf(tilt);


					float cosine = fabs(x_dir*xx + y_dir*yy + z_dir*zz);
					if (cosine>=cosAngle)
					{
						cosine = expf( -((cosine -1)*(cosine -1))*aux );
						w += cosine*( dAi(resDirFSC, k) );
						wt += cosine;
					}
				}

				double wRes = w/wt;
				{
					MDRowVec row;
					row.setValue(MDL_ANGLE_ROT, (double) i);
					row.setValue(MDL_ANGLE_TILT, (double) j);
					row.setValue(MDL_RESOLUTION_FRC, wRes);
					mdOut.addRow(row);
				}
			}
		}
    }
    
    '''
