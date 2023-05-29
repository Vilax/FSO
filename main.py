import os.path
import time
import sys
import mrcfile
import argparse
import numpy as np
import estimation as est

parser = argparse.ArgumentParser(prog=sys.argv[0],
                                 description='Calculate Fourier Shell Occupancy - FSO curve - via directional FSC measurements.',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
                                 add_help=True)

parser.add_argument('-half1', '--half1', type=str, required=True, help='Input half map 1')
parser.add_argument('-half2', '--half2', type=str, required=True, help='Input half map 2')
parser.add_argument('-sampling', '--sampling', type=float, required=False, default=1.0,
                    help='Pixel size (Angstrom). If it is not provided by default will be 1 A/px.')
parser.add_argument('-mask', '--mask', type=str, required=False,
                    help='(Optional) Smooth mask to remove noise. If it is not provided, the computation will be carried out without mask.')
parser.add_argument('-anglecone', '--anglecone', type=float, required=False, default=17.0,
                    help="(Optional) Angle Cone in degrees (angle between the axis and the  generatrix) for estimating the directional FSC")
parser.add_argument('-o', '--output', type=str, required=True, help="Folder where the results will be stored.")
parser.add_argument('-t', '--threads', required=False, default=1, help="(Optional) Number of threads to be used")
parser.add_argument('-threshold', '--threshold', type=float, required=False, default=0.143,
                    help="(Optional) Threshold for the FSC/directionalFSC estimation")


def main():

    args = parser.parse_args()

    #halfMap1 = mrcfile.open(args.halfmap1, mode='r')
    #halfMap2 = mrcfile.open(args.halfmap2, mode='r')

    #halfMap1Data = np.copy(halfMap1.data)
    #halfMap2Data = np.copy(halfMap2.data)

    est.run(args.half1, args.half2, args.mask, args.sampling, args.anglecone, args.threshold)




if (__name__ == "__main__"):
	main()
