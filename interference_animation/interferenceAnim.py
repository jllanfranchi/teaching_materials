#!/usr/bin/env python

#
# Justin Lanfranchi
# 2010.11.06
#
# Tested in Python 2.6.5 in Linux; should work in 2.4+ with appropriate modules
# (scipy, numpy, and matplotlib); not sure about 3.0. Should port to other OS
# but the mencoder (animations) might not work properly; these can be turned
# off with the appropriate argument being set to the animateInterference
# function: animate=False instead of animate=True
#
# REQUIRES mencoder TO PRODUCE ANIMATIONS, which is included with mplayer,
# http://www.mplayerhq.hu/design7/news.html
#
#

from __future__ import division

#-- Standard python modules
import os, sys, subprocess

#-- Add-on modules
import scipy
from numpy import *
from matplotlib import mlab


def efield(r, k,  omega, t, a=1, phi=0):
    """
    compute e-field at distance(s) r from the source; plane-wave approximation
    means NO reduction in amplitude for varying distances.
    """
    return a*sin(k*r - omega*t + phi)

def centerMark(R, A, circRad):
    """
    put a marker into the array A around the locations where the array R=0;
    makes sense for scalar radial field R. Assumes that A is in the range [0,1]
    where 0 => black and 1 => white. If A is in another scale, results will
    not be what you expect.
    """
    a = A.flatten()
    
    #-- Find pixels within circRad of center; paint them black
    centerCircle = mlab.find(R <= circRad)
    a[centerCircle] = 0
    
    #-- Find pixels within (3/4)*circRad of center; paint them white
    centerPoint = mlab.find(R < circRad*3/4)
    a[centerPoint] = 1
    
    return a.reshape(A.shape)

def animateInterference(sourceLoc=[[0,2.5],[0,-2.5]], lam=1, phi=0,
                        xRange=[-10,10], yRange=[-10,10],
                        res=[600,600], nFramesPerPeriod=20, fps=15,
                        renormalize=False, animate=True,
                        basePath='interference_animation'):
    speedOfLight = 299792458.0
    frameNumFmt = '05d'
    frameExtn = '.jpg'
    lambdaFmt = '-05.2f'
    sepFmt = '-06.3f'
    nSrcFmt = '02d'

    hpix = res[0]
    vpix = res[1]

    xmin = xRange[0]
    xmax = xRange[1]
    
    ymin = yRange[0]
    ymax = yRange[1]

    dx = (xmax-xmin)/(hpix-1)
    dy = (ymax-ymin)/(vpix-1)

    x = arange(xmin, xmax+dx, dx)
    y = arange(ymin, ymax+dy, dy)
    X, Y = meshgrid(x, y)

    nSources = len(sourceLoc)

    R = []
    print "  source locations:", sourceLoc
    for loc in sourceLoc:
        R.append( sqrt((X-loc[0])**2 + (Y-loc[1])**2) )

    #-- If user proveds scalar argument, make into array of equal elements
    if isscalar(phi):
        p = []
        for n in range(nSources):
            p.append(phi)
        phi = p
    phi = array(phi)

    #-- If user proveds scalar argument, make into array of equal elements
    if isscalar(lam):
        l = []
        for n in range(nSources):
            l.append(lam)
        lam = l
    lam = array(lam)
    print "  lambda:", lam

    #-- compute frequencies [Hz]
    nu = speedOfLight/lam
    
    #-- compute periods, [s]
    T = 1/nu
    
    #-- compute angular frequencies, [rad/s]
    omega = 2*pi*nu
    
    #-- compute wave number, [rad/m]
    k = 2*pi/lam
    
    #-- figure out how many samples to take to get good results when the
    #   animation is looped (without using too many frames, i.e., for non-
    #   commensurate frequencies)
    maxT = T.max()
    minT = T.min()

    maxTind = mlab.find(T==maxT)[0]
    minTind = mlab.find(T==minT)[0]

    trialPeriods = arange(1,20,1)
    remainder = []
    testT = list(T[0:minTind])
    testT.extend(T[min([minTind+1,len(T)-1]):])
    testT = array(testT)
    for trialPeriod in trialPeriods:
        remainder.append(sum(mod(minT*trialPeriod,testT)))
    remainder = array(remainder)
    minInd = mlab.find(remainder == remainder.min())[0]
    lcT = trialPeriods[minInd]*minT
    
    nFrames = nFramesPerPeriod * (lcT/minT)
    print "  total frames:", int(nFrames)
    
    tmin = 0
    tmax = lcT
    dt = (tmax-tmin)/nFrames
    
    print "  creating frames... "
    sys.stdout.flush()
   
    #-- Create target directory if it doesn't exist
    if not os.path.isdir(basePath):
        os.mkdir(basePath)
    
    #-- Create frame(s) for each time point t
    filesCreated = []
    frameNumber = -1
    Iaggr = zeros_like(R[0])
    for t in arange(tmin, tmax, dt):
        frameNumber += 1
        
        sys.stdout.write(str(frameNumber))
        sys.stdout.flush()
       
        #-- compute E-field
        E = zeros_like(R[0])
        for n in range(nSources):
            E += efield(R[n], k[n], omega[n], t, a=1, phi=phi[n])
        
        #-- compute intensity
        I = E**2

        Iaggr += I

        #-- normalize intensity to range of [0,1]
        if renormalize:
            Imax = I.max()
        else:
            Imax = nSources**2
        I = I/Imax
        #for n in range(nSources):
        #    I = centerMark(R[n], I, 4*dx)
        
        #-- file name for this frame
        fname = 'frame_' + format(frameNumber, frameNumFmt) + frameExtn
        fullFname = os.path.join(basePath, fname)
        #print fullFname
        
        sys.stdout.write(".")
        sys.stdout.flush()
   
        if animate or frameNumber == 0:
            #-- save image to file
            scipy.misc.imsave(fullFname, I)
        
            #-- record that the image file has been created
            filesCreated.append(fullFname)

        sys.stdout.write(". ")
        sys.stdout.flush()
   
    print filesCreated

    #-- Create a sensible naming scheme depending upon how many sources are
    #   present...
    #    1 source:  one wavelength to report, no separation to report
    #    2 sources: two wavelengths, single separation
    #   >2 sources: report just the first wavelength and the smallest
    #               separation among the sources (makes most sense for, e.g.,
    #               regular polygons or uniform arrays)
    if nSources == 1:
        outFname = '__lambda_' + format(lam[0], lambdaFmt)

    elif nSources == 2:
        r = []
        for n in range(nSources):
            for m in range(nSources):
                if n != m:
                    r.append(sqrt(sum((array(sourceLoc[m]) -
                                       array(sourceLoc[n]))**2)) )
        r = array(r)
        rMin = r.min()
        outFname = '__sep_' + format(rMin, sepFmt) + \
                '__lambda1_' + format(lam[0], lambdaFmt) + \
                '__lambda2_' + format(lam[1], lambdaFmt)
    else:
        r = []
        for n in range(nSources):
            for m in range(nSources):
                if n != m:
                    r.append(sqrt(sum((array(sourceLoc[m]) -
                                       array(sourceLoc[n]))**2)) )
        r = array(r)
        rMin = r.min()
        outFname = '__nsrc_' + format(nSources, nSrcFmt) + \
                '__lambda_' + format(lam[0], lambdaFmt) + \
                '__minsep_' + format(rMin, sepFmt)

    #-- create all file names based upon naming scheme above & base path
    animFname = os.path.join(basePath, 'anim' + outFname + '.avi')
    frame0Fname = os.path.join(basePath,
                               'frame_' + format(0, frameNumFmt) + frameExtn)
    stillFname = os.path.join(basePath,
                              'still_' + outFname + frameExtn)
    avgIntensityFname = os.path.join(basePath,
                              'avg_intensity_' + outFname + frameExtn)

    #-- NOTE: this requires mencoder to work
    if animate:
        sys.stdout.write("\nEncoding video... ")
        sys.stdout.flush()
        p = os.popen3('mencoder "mf://' +
                      os.path.join(basePath, 'frame_*' + frameExtn) +
                      '" -mf fps=' + str(int(fps)) +
                      ' -o ' + animFname +
                      ' -ovc lavc' +
                      ' -lavcopts vcodec=mpeg4')
    
        trash = p[1].read()
    
        sys.stdout.write("\n\nDone.\n")
        sys.stdout.flush()

    #-- rename the first frame so it becomes the "still" representing the case
    #   being demonstrated
    os.rename(frame0Fname, stillFname)

    #-- save average intensity image to file
    scipy.misc.imsave(avgIntensityFname, Iaggr)
     
    #-- erase all other frames
    for f in filesCreated[1:]:
        os.remove(f)

#==============================================================================
#
#
# Begin scripting portion of program... produce images & animations for
# various scenarios.
#
#
#==============================================================================

#==============================================================================
# Define parameters
#==============================================================================
vpix = 600
hpix = 600

xmin = -5
xmax = 5

ymin = -5
ymax = 5

vsep = 1.0
hsep = 0


#==============================================================================
# Varying lambda, animation
#==============================================================================

#nFramesPerPeriod = 20
#lam = [ .25, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 5, 10 ]
#for l in lam:
#    animateInterference(sourceLoc=[[0,vsep/2],[0,-vsep/2]], lam=l,
#                        xRange=[xmin,xmax], yRange=[ymin,ymax],
#                        res=[hpix,vpix], nFramesPerPeriod=nFramesPerPeriod,
#                        fps=15, animate=True,
#                        basePath=os.path.join('interference_animation',
#                                              'equal_freq'))


#==============================================================================
# More finely-varying lambda, stills only (no animation)
#==============================================================================

#lam = arange(0.1,1,.02)
#for l in lam:
#    animateInterference(sourceLoc=[[0,vsep/2],[0,-vsep/2]], lam=l,
#                        xRange=[xmin,xmax], yRange=[ymin,ymax],
#                        res=[hpix,vpix], animate=False, nFramesPerPeriod=1,
#                        basePath=os.path.join('interference_animation',
#                                              'equal_freq'))


#==============================================================================
# Varying separation, constant (and equal) wavelengths
#==============================================================================

#nFramesPerPeriod = 15
#spacings = arange(0.1,5,.1)
#for spacing in spacings:
#    animateInterference(sourceLoc=[[0,spacing/2],[0,-spacing/2]], lam=1.0,
#                        xRange=[xmin,xmax], yRange=[ymin,ymax],
#                        res=[hpix,vpix], nFramesPerPeriod=nFramesPerPeriod,
#                        fps=15, animate=True,
#                        basePath=os.path.join('interference_animation',
#                                              'spacing_variation'))


#==============================================================================
# Interference between two sources with different frequencies
#==============================================================================

#nFramesPerPeriod = 15
#lam = [ [1,1.1], [1,1.25], [1,1.5], [1,1.75], [1,2], [1,3]]
#for l in lam:
#    animateInterference(sourceLoc=[[0,vsep/2],[0,-vsep/2]], lam=l,
#                        xRange=[xmin,xmax], yRange=[ymin,ymax],
#                        res=[hpix,vpix], nFramesPerPeriod=nFramesPerPeriod,
#                        fps=30, animate=True,
#                        basePath=os.path.join('interference_animation',
#                                              'diff_freq'))


#==============================================================================
# More than 2 sources
#==============================================================================
hpix = 1280
vpix = 800
xmin = 10
xmax = 100
ymin = -15
ymax = 15
nFramesPerPeriod = 5

lam = [.05]
loc = [[-.5,.5],[-.5,-.5],[.5,.5],[.5,-.5]]
loc = [[0,1.5],[0,.5],[0,-.5],[0,-1.5]]
loc = [[0,3.5],[0,2.5],[0,1.5],[0,.5],[0,-.5],[0,-1.5],[0,-2.5],[0,-3.5]]
loc = [[0,3.5],[0,2.5],[0,1.5],[0,.5],[0,-.5],[0,-1.5],[0,-2.5],[0,-3.5]]
#y = arange(-10.5,11,.5)
#x = zeros_like(y)
#loc = [list(elem) for elem in zip(list(x),list(y))]

#xloc = lam[0]/4*cos(arange(0,2*pi,2*pi/8)+2*pi/16)
#yloc = lam[0]/4*sin(arange(0,2*pi,2*pi/8)+2*pi/16)
#loc = zip(xloc,yloc)
#phi = [pi/2, pi/4, -pi/4, 0]
phi = 0
scaleFactors = arange(.001,.011,.001)
scaleFactors = [1]
for l in lam:
    dl = l/15
    for scaleFactor in scaleFactors:
        print "scaleFactor:", scaleFactor
        locArray = array(loc)*scaleFactor
        scaledLoc = [ list(elem) for elem in list(locArray) ]
        animateInterference(sourceLoc=scaledLoc,
                            lam=l, phi=phi,
                            xRange=[xmin,xmax], yRange=[ymin,ymax],
                            res=[hpix,vpix],
                            nFramesPerPeriod=nFramesPerPeriod,
                            renormalize=True, fps=15, animate=True,
                            basePath=os.path.join('interference_animation',
                                              'multiple_sources'))
