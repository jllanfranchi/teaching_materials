#!/usr/bin/env python

from __future__ import division

import sys
import os
import re
import scipy as sp
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import pylab as pyl

def sciFormat(x, dec):
    l = sp.log10(np.float96(x))
    lf = float(np.floor(l))
    if l > 5:
        m = float(np.round(x/10**lf, dec))
        return r"$" + format(m, '.'+format(int(dec))+'f') + r" \times 10^{" + \
                format(int(lf),'d') + r"}$"
    else:
        return format(x)

def smartFormat(x, dec):
    if np.isinf(x):
        return r"$\infty$"
    elif np.isnan(x):
        return r"---"
    else:
        return format(float(x), '.'+format(int(dec),'d')+'f')

#-- User-defined constants
Ntot = 100
rowsToPrint = [100, 99, 98, 97, 52, 51, 50, 49, 48, 1, 0]

#-- Convert all values to long ints
Ntot = long(Ntot)

#-- Define all Nup values possible
all_Nup = range(Ntot,-1,-1)

#-- Table header
lines = []
headings = [r"N_{\uparrow}", r"U/\mu B", r"M/N\mu", r"\Omega", r"S/k",
                r"kT/\mu B", r"C/Nk"]
nel = len(headings)
header = r"$" + r"$ & $".join(headings) + r"$ \\ \midrule \addlinespace[5pt]"
lines.append(r"\begin{tabular}{rrrcrrc}")
lines.append(header)

tableRows = []
for Nup in all_Nup:
    Ndown = np.float96(Ntot - Nup)
    U_by_mu_B = np.float96(Ntot - 2*Nup)
    M_by_N_mu = np.float96(Nup-Ndown)/np.float96(Ntot)
    Omega = sp.comb(Ntot, Nup, exact=True)
    S_by_k = np.log(np.float96(Omega))
    tableRows.append( [Nup, U_by_mu_B, M_by_N_mu, Omega, S_by_k] )

rowNum = 0
for row in tableRows:
    if rowNum == 0 or rowNum == Ntot:
        kT_by_mu_B = 0
    else:
        kT_by_mu_B = (tableRows[rowNum+1][1]-tableRows[rowNum-1][1]) / \
                (tableRows[rowNum+1][4]-tableRows[rowNum-1][4])
    tableRows[rowNum].append( kT_by_mu_B )
    rowNum += 1

rowNum = 0
for row in tableRows:
    if rowNum == 0 or rowNum == Ntot:
        C_by_N_k = np.nan
    else:
        U1 = tableRows[rowNum+1][1]
        U0 = tableRows[rowNum-1][1]
        T1 = tableRows[rowNum+1][5]
        T0 = tableRows[rowNum-1][5]
        T_ = tableRows[rowNum][5]
        if np.inf in [T_, T0, T1]:
            C_by_N_k = np.nan
        else:
            C_by_N_k = (U1-U0)/(T1-T0)/Ntot
    tableRows[rowNum].append( C_by_N_k )
    rowNum += 1

rowNum = 100
lastPrinted = True
for row in tableRows:
    if not rowNum in rowsToPrint:
        if lastPrinted:
            strVals = [r"\vdots"]*7
            line = r"\addlinespace[-5pt]" + \
                    r" & ".join(strVals) + r" \\ \addlinespace[5pt]"
            lastPrinted = False
        else:
            lastPrinted = False
            rowNum -= 1
            continue
    else:
        lastPrinted = True
        Nup = row[0]
        U_by_mu_B = row[1]
        M_by_N_mu = row[2]
        Omega = row[3]
        S_by_k = row[4]
        kT_by_mu_B = row[5]
        C_by_N_k = row[6]

        strVals = []
        strVals.append( format(Nup) )
        strVals.append( format(U_by_mu_B) )
        strVals.append( format(float(M_by_N_mu), '.2f') )
        strVals.append( sciFormat(Omega, 1) )
        strVals.append( format(float(S_by_k), '.2f') )
        strVals.append( smartFormat(kT_by_mu_B, 2) )
        strVals.append( smartFormat(C_by_N_k, 3) )

        line = r" & ".join(strVals) + r" \\ \addlinespace[5pt]"
    lines.append(line)
    rowNum -= 1

footer = r"\end{tabular}"
lines.append(footer)

[ sys.stdout.write(line + "\n") for line in lines ]
sys.stdout.flush()

print ""

Nup =           np.array([row[0] for row in tableRows])
U_by_mu_B =     np.array([row[1] for row in tableRows])
M_by_N_mu =     np.array([row[2] for row in tableRows])
Omega =         np.array([row[3] for row in tableRows])
S_by_k =        np.array([row[4] for row in tableRows])
kT_by_mu_B =    np.array([row[5] for row in tableRows])
C_by_N_k =      np.array([row[6] for row in tableRows])
C_by_N_k[0] = 0
C_by_N_k[-1] = 0

mpl.rcParams['ytick.direction']='out'
mpl.rcParams['xtick.direction']='out'
mpl.rcParams['figure.subplot.left']=.14
mpl.rcParams['figure.subplot.bottom']=.14
mpl.rcParams['interactive']=True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 10.0

fig = plt.figure(1, figsize=(5,4), dpi=90, facecolor='w', edgecolor='k')
ax = plt.axes(axisbg='w')
plt.clf()
plt.plot(U_by_mu_B, S_by_k, 'k-', linewidth=1)
plt.title(r"Entropy vs. Energy")
plt.grid(False)
ax = pyl.gca()

ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.spines['top'].set_position(('data',-1))
ax.spines['right'].set_position(('data',-1))

plt.xlim(-105,105)
plt.ylim(0,75)

plt.xticks(np.arange(-100,101,50), fontsize=10, family='serif')
plt.yticks(np.arange(0,70,20), fontsize=10, family='serif')
plt.minorticks_on()

yax = ax.get_yaxis()
yax.minor.formatter.set_locs (np.arange (0,71,10))
yax.set_ticks_position('left')
yax.set_visible(True)

xax = ax.get_xaxis()
xax.set_ticks_position('bottom')
xax.set_visible(True)

plt.xlabel(r"$U/\mu B$")
plt.ylabel(r"$S/k$")
plt.savefig('paramagnet_entropy_vs_energy.pdf')

fig = plt.figure(2, figsize=(5,4), dpi=90, facecolor='w', edgecolor='k')
ax = plt.axes(axisbg='w')
plt.clf()
plt.plot(U_by_mu_B/Ntot, kT_by_mu_B, 'k-', linewidth=1)
plt.title(r"Temperature vs. Energy")
plt.grid(False)
ax = pyl.gca()

ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)

ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)

ax.spines['top'].set_position(('data',-1))
ax.spines['right'].set_position(('data',-1))

plt.xlim(-1,1)
plt.ylim(-20,20)

plt.xticks(np.arange(-1,1.1,1), fontsize=10, family='serif')
plt.yticks(np.arange(-20,21,10), fontsize=10, family='serif')
plt.minorticks_on()

yax = ax.get_yaxis()
yax.minor.formatter.set_locs (np.arange (0,71,10))
yax.set_ticks_position('left')
yax.set_visible(True)

xax = ax.get_xaxis()
xax.set_ticks_position('bottom')
xax.set_visible(True)

plt.xlabel(r"$U/N\mu B$")
plt.ylabel(r"$kT/\mu B$")
plt.savefig('paramagnet_temp_vs_energy.pdf')
plt.show()

fig = plt.figure(3, figsize=(5,4), dpi=90, facecolor='w', edgecolor='k')
ax = plt.axes(axisbg='w')
plt.clf()
plt.plot(kT_by_mu_B, C_by_N_k, 'k-', linewidth=1)
plt.title(r"Heat Capacity vs. Temperature")
plt.grid(False)
ax = pyl.gca()

ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)

plt.xlim(0,7.25)
plt.ylim(0,.5)

plt.xticks(np.arange(0,7.1,1), fontsize=10, family='serif')
plt.yticks(np.arange(0.1,.51,.1), fontsize=10, family='serif')
plt.minorticks_off()

yax = ax.get_yaxis()
yax.set_ticks_position('left')
yax.set_visible(True)

xax = ax.get_xaxis()
xax.set_ticks_position('bottom')
xax.set_visible(True)

plt.xlabel(r"$kT/\mu B$")
plt.ylabel(r"$C/Nk$")
#plt.savefig('paramagnet_heatcap_vs_temp.pdf')
plt.show()

fig = plt.figure(4, figsize=(5,4), dpi=90, facecolor='w', edgecolor='k')
ax = plt.axes(axisbg='w')
plt.clf()
plt.plot(kT_by_mu_B, M_by_N_mu, 'k-', linewidth=1)
plt.title(r"Magnetization vs. Temperature")
plt.grid(False)
ax = pyl.gca()

ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)

#ax.spines['bottom'].set_position('zero')
#ax.spines['left'].set_position('zero')
ax.spines['top'].set_position(('data',-1))
ax.spines['right'].set_position(('data',-1))

plt.xlim(-10.25,10.25)
plt.ylim(-1.1,1.1)

plt.xticks(np.arange(-10,10.1,5), fontsize=10, family='serif')
plt.yticks(np.arange(-1,1.1,1), fontsize=10, family='serif')
plt.minorticks_on()

yax = ax.get_yaxis()
yax.set_ticks_position('left')
yax.set_visible(True)

xax = ax.get_xaxis()
xax.set_ticks_position('bottom')
xax.set_visible(True)

plt.xlabel(r"$kT/\mu B$")
plt.ylabel(r"$M/N\mu$")
plt.savefig('paramagnet_magnetization_vs_temp.pdf')
plt.show()


