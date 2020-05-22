#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 11:22:57 2019

# @author: jlvilas
"""

import argparse
import plotOutput as pltOut

my_parser = argparse.ArgumentParser()
my_parser.add_argument('--input', action='store', type=str, required=True)
my_parser.add_argument('--plot_type', action='store', type=str, required=True)
my_parser.add_argument('--labels', action='store', nargs='*', type=str, required=True)
my_parser.add_argument('--xlabel', action='store', type=str, required=True)
my_parser.add_argument('--ylabel', action='store', type=str, required=True)
my_parser.add_argument('--title', action='store', type=str, required=True)

args = my_parser.parse_args()
print(args)

title = args.title
xlabel = args.xlabel
ylabel = args.ylabel
"""

pltOut.plotFSC("/home/vilas/build-OFSC-Desktop_Qt_5_13_2_GCC_64bit-Debug/results/GlobalFSC.xmd", "_resolutionFreqFourier", "_resolutionFRC", "resolution", "caca", "DirectionalResolution")


pltOut.plotPolar("/home/vilas/build-OFSC-Desktop_Qt_5_13_2_GCC_64bit-Debug/results/DirectionalResolution.xmd", "_angleTilt", "_angleRot", "_resolutionFRC", "resolution", "caca", "DirectionalResolution")
"""
if args.plot_type == 'FSCplot':
    pltOut.plotFSC(args.input, args.labels[0], args.labels[1], xlabel, ylabel, title)

if args.plot_type == 'FOSplot':
    pltOut.plotFOS(args.input, args.labels[0], args.labels[1], xlabel, ylabel, title)

if args.plot_type == 'XYplot':
    pltOut.plotXY(args.input, args.labels[0], args.labels[1], xlabel, ylabel, title)

if args.plot_type == 'polarplot':
    pltOut.plotPolar(args.input, args.labels[0], args.labels[1], args.labels[2], xlabel, ylabel, title)

if args.plot_type == 'particleDistribution':
    pltOut.plotParticleDistribution(args.input, args.labels[0], args.labels[1], args.labels[2], xlabel, ylabel, title)
