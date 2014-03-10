# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import division

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from matplotlib.tri import Triangulation, UniformTriRefiner,\
    CubicTriInterpolator
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as P3D
import numpy as np
import time
from numpy import *

# <codecell>

#%pylab qt4
plt.ion()

# <codecell>

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

# <codecell>

def sph2cart(rho, theta, phi):
    x = rho * sin(theta) * cos(phi)
    y = rho * sin(theta) * sin(phi)
    z = rho * cos(theta)
    return x, y, z

def pol2cart(rho, theta):
    x = rho * cos(theta)
    y = rho * sin(theta)
    return x, y

# <codecell>

def polVolDiffelVerts(r, theta, z, dr, dtheta, dz, ds=None ):
    if ds == None or ds <= 0:
        ds = dr/2
        
    front, back, top, bottom, inside, outside = (True,)*6
    polys = []
    if r <= dr/2:
        r0 = 0
        inside = False
    
    if dtheta >= 2*np.pi:
        dtheta = 2*np.pi
        front = False
        back = False
        
    if front:
        R = [r-dr/2, r+dr/2, r+dr/2, r-dr/2]
        THETA = [theta-dtheta/2]*4
        Z = [z-dz/2, z-dz/2, z+dz/2, z+dz/2]
        X, Y = pol2cart(R, THETA)
        polys.append(zip(X,Y,Z))
        
    if back:
        R = [r-dr/2, r+dr/2, r+dr/2, r-dr/2]
        THETA = [theta+dtheta/2]*4
        Z = [z-dz/2, z-dz/2, z+dz/2, z+dz/2]
        X, Y = pol2cart(R, THETA)
        polys.append(zip(X,Y,Z))
        
    if inside:
        nRectInside = np.max([np.ceil((r-dr/2)*dtheta/ds),2])
        dtheta_ = dtheta / nRectInside
        for theta_ in np.linspace(theta-dtheta/2, theta+dtheta/2, nRectInside, endpoint=False):
            R = [r-dr/2]*4
            THETA = [theta_, theta_+dtheta_, theta_+dtheta_, theta_]
            Z = [z-dz/2, z-dz/2, z+dz/2, z+dz/2]
            X, Y = pol2cart(R, THETA)
            polys.append(zip(X,Y,Z))
            
    if outside:
        nRectOutside = np.max([np.ceil((r+dr/2)*dtheta/ds),2])
        dtheta_ = dtheta / nRectOutside
        for theta_ in np.linspace(theta-dtheta/2, theta+dtheta/2, nRectOutside, endpoint=False):
            R = [r+dr/2]*4
            THETA = [theta_, theta_+dtheta_, theta_+dtheta_, theta_]
            Z = [z-dz/2, z-dz/2, z+dz/2, z+dz/2]
            X, Y = pol2cart(R, THETA)
            polys.append(zip(X,Y,Z))
    
    if top:
        R = []
        THETA = []
        Z = []
        if inside:
            for theta_ in np.linspace(theta+dtheta/2, theta-dtheta/2, nRectInside+1, endpoint=True):
                R.append(r-dr/2)
                THETA.append(theta_)
                Z.append(z+dz/2)
            #if dtheta >= 2*np.pi:
            #    R.pop()
            #    THETA.pop()
            #    Z.pop()
        elif front:
            R.append(0)
            THETA.append(0)
            Z.append(z+dz/2)

        #-- There's *always* an outside!
        for theta_ in np.linspace(theta-dtheta/2, theta+dtheta/2, nRectOutside+1, endpoint=True):
            R.append(r+dr/2)
            THETA.append(theta_)
            Z.append(z+dz/2)

        X, Y = pol2cart(R, THETA)
        polys.append(zip(X,Y,Z))

    if bottom:
        R = []
        THETA = []
        Z = []
        if inside:
            for theta_ in np.linspace(theta+dtheta/2, theta-dtheta/2, nRectInside+1, endpoint=True):
                R.append(r-dr/2)
                THETA.append(theta_)
                Z.append(z-dz/2)
            #if dtheta >= 2*np.pi:
            #    R.pop()
            #    THETA.pop()
            #    Z.pop()

        elif front:
            R.append(0)
            THETA.append(0)
            Z.append(z-dz/2)

        #-- There's *always* an outside!
        for theta_ in np.linspace(theta-dtheta/2, theta+dtheta/2, nRectOutside+1, endpoint=True):
            R.append(r+dr/2)
            THETA.append(theta_)
            Z.append(z-dz/2)

        X, Y = pol2cart(R, THETA)
        polys.append(zip(X,Y,Z))
        
    return polys

# <codecell>

R = 10
Z = 30

#PERSP = "XSIDE"
PERSP = "YSIDE"
#PERSP = "ISO"

plt.close(1)
if PERSP == "XSIDE":
    fig = plt.figure(1, figsize=(8,8))
    fig.clf()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=0*Z, azim=0)
    ax.set_aspect(0.65)
elif PERSP == "YSIDE":
    fig = plt.figure(1, figsize=(8,8))
    fig.clf()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=0*Z, azim=270)
    ax.set_aspect(0.65)
elif PERSP == "ISO":
    fig = plt.figure(1, figsize=(8,6))
    fig.clf()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=1.1*Z, azim=22.5)
else:
    raise Exception("Pick 'XSIDE', 'YSIDE', or 'ISO'")

ax.grid(b=False)
ax.set_axis_off()

#-- Add 3 vectors for nicer axes
xmin=-30;xmax=30;ymin=-30;ymax=30;zmin=-15;zmax=45
xax = Arrow3D([xmin,xmax],[0,0],[0,0],
               mutation_scale=10, lw=1, arrowstyle='->', color="gray",
               alpha=0.5, zorder=0.003)
yax = Arrow3D([0,0],[ymin,ymax],[0,0],
               mutation_scale=10, lw=1, arrowstyle='->', color="gray",
               alpha=0.5, zorder=0.001)
zax = Arrow3D([0,0],[0,0],[zmin,zmax],
               mutation_scale=10, lw=1, arrowstyle='->', color="gray",
               alpha=0.5, zorder=0.002)
ax.add_artist(xax)
ax.add_artist(yax)
ax.add_artist(zax)


origin = ax.plot3D([0],[0],[0],  'o', color='gray', markersize=3, zorder=3)



#-- Add sphere, shaded wireframe
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

x = R * np.outer(np.cos(u), np.sin(v))
y = R * np.outer(np.sin(u), np.sin(v))
z = R * np.outer(np.ones(np.size(u)), np.cos(v))
sph = ax.plot_surface(x, y, z,  rstride=4, cstride=4,
                      color=[0.5]*3, edgecolor=(0,0,0,0.5), alpha=0.1,
                      linewidth=0.1, shade=True, antialiased=True)

#-- Add point at which evaluating E (r)
point = ax.plot3D([0],[0],[Z],  'ro', markersize=5)

chunk = ax.plot_surface([0,1,1,0],[0,0,1,1],[0,0,0,0])

E_x0 = 0
E_y0 = 0
E_z0 = Z

r_x0 = 0
r_y0 = 0
r_z0 = 0

r_x1 = 0
r_y1 = 0
r_z1 = Z


r_vec = Arrow3D([0,r_x1],[0,r_y1],[0,r_z1],
               mutation_scale=20, lw=2, arrowstyle='-|>', color="r", zorder=0.02,
               alpha=0.8)

ri_vec = Arrow3D([0,r_x0],[0,r_y0],[0,r_z0],
               mutation_scale=10, lw=2, arrowstyle='-|>', color="k", zorder=0.8,
               alpha=0.8)

rp_vec = Arrow3D([0,r_x1],[0,r_y1],[0,r_z1],
               mutation_scale=20, lw=2, arrowstyle='-|>', color="b", zorder=0.9,
               alpha=0.8)

#r_pt, = ax.plot3D([r_x0],[r_y0],[r_z0],  'ko', markersize=5)

Ei_color = (0,0.5,0.5)
Ei_vec = Arrow3D([0,0],[0,0],[30,40],
               mutation_scale=15, lw=2, arrowstyle='-|>', color=E_color)

polys = polVolDiffelVerts(R-R/20, pi/2, 0, R/10, pi/20, R/10)
#diffVolEl = P3D(polys, linewidth=0.2, facecolor=(1,0.3,0.1), alpha=0.8)
diffVolEl = P3D(polys, linewidth=0.2, facecolor=(1,0.3,0.1), alpha=0.6,zorder=0.015)

polys = polVolDiffelVerts(R-R/2, 0, 0, R, 2*pi, R/10, R/10)
diffDisk = P3D(polys, linewidth=0.05, facecolor=(1,0.3,0.1), alpha=0.1,zorder=0.012)

polys = polVolDiffelVerts(R-R/2, 0, 0, R/8, 2*pi, R/10, R/10)
diffTorus = P3D(polys, linewidth=0.1, facecolor=None, alpha=0.0,zorder=0.013)

ax.add_artist(r_vec)
ax.add_artist(ri_vec)
ax.add_artist(rp_vec)
ax.add_artist(Ei_vec)
ax.add_collection3d(diffDisk)
ax.add_collection3d(diffTorus)
ax.add_collection3d(diffVolEl)

if PERSP == "XSIDE":
    ax.text(0, ymax+1, 0, r"$y$", ha='center', va='center')
    ax.text(0, 0, zmax+1, r"$z$", ha='center', va='center')
    rp_txt = ax.text(0, 2, Z*.75, r"$\vec{\mathscr{r}}_i=\vec r - \vec r_i$",
                     size=16, ha='left', va='center', color='b', zorder=1)
    Ei_txt = ax.text(0,0,40, r"$\vec {E_i}$",
                     size=16, ha='center', va='center', color=E_color, zorder=1)
    ri_txt = ax.text(2, 1, -1, r"$\vec r_i$",
                     size=16, ha='left', va='center', color='k', zorder=1)
    r_txt = ax.text(0, 2, Z/2, r"$\vec r$",
                   size=16, ha='center', va='center', color='r', zorder=1)

if PERSP == "YSIDE":
    ax.text(xmax+1, 0, 0, r"$x$", ha='center', va='center')
    ax.text(0, 0, zmax+1, r"$z$", ha='center', va='center')
    rp_txt = ax.text(2, 2, Z*.75, r"$\vec{\mathscr{r}}_i=\vec r - \vec r_i$",
                     size=16, ha='left', va='center', color='b', zorder=1)
    Ei_txt = ax.text(0,0,40, r"$\vec {E_i}$",
                     size=16, ha='center', va='center', color=E_color, zorder=1)
    ri_txt = ax.text(2, 1, -2, r"$\vec r_i$",
                     size=16, ha='left', va='center', color='k', zorder=1)
    r_txt = ax.text(2, 2, Z/2, r"$\vec r$",
                   size=16, ha='center', va='center', color='r', zorder=1)

if PERSP == "ISO":
    ax.text(xmax+1, 1, -1, r"$x$", ha='center', va='center')
    ax.text(0, ymax+1, 0, r"$y$", ha='center', va='center')
    ax.text(0, 0, zmax+1, r"$z$", ha='center', va='center')
    rp_txt = ax.text(0, 2, Z*.75, r"$\vec{\mathscr{r}}_i=\vec r - \vec r_i$",
                     size=16, ha='left', va='center', color='b', zorder=1)
    Ei_txt = ax.text(0,0,40, r"$\vec {E_i}$",
                     size=16, ha='center', va='center', color=E_color, zorder=1)
    ri_txt = ax.text(2, 1, -1, r"$\vec r_i$",
                     size=16, ha='left', va='center', color='k', zorder=1)
    r_txt = ax.text(0, 2, Z/2, r"$\vec r$",
                   size=16, ha='center', va='center', color='r', zorder=1)

    eqn = ax.text(-10,5,30, 
                  r"$\mathrm{At\,each\,step:}$"
                  +"\n"
                  +r"$\vec{E_i}(\vec{r}) = k\,\frac{\rho(\vec r_i)\,\mathrm{d}V_i}{\|\|\vec{\mathscr{r}}_i\|\|^2}"
                  + r"\,\hat{\mathscr{r}}_i$",
                  size=16)
    eqn2 = ax.text(10,5,-15,
                   r"$\mathrm{Overall\,operation:}$"
                   +"\n"
                   +r"$\vec{E}(\vec{r}) = "
                   +r"\int_{z_i=-R}^{R}\,"
                   +r"\int_{\varrho_i=0}^{\sqrt{R^2-z^2}}"
                   +r"\int_{\theta_i=0}^{2\pi}"
                   +r"\left( k\,\frac{\rho(\vec r_i)\,"
                   +r"\left( \varrho_i \mathrm{d}\theta_i\,\mathrm{d}\varrho_i\,\mathrm{d}z_i \right)"
                   +r"}{\|\|\vec{\mathscr{r}}_i\|\|^2}"
                   + r"\,\hat{\mathscr{r}}_i\right)$",
                   ha="center", va="top",
                   size=14)

ax.set_xlim(left=-30,right=30)
ax.set_ylim(bottom=-30, top=30)

thetaStep = pi/4
rStep = R/4

rhoStepTgt = R/5
dsStepTgt = R/5
dzStepTgt = R/10

phiStep = pi/4
plt.show()

nZSamp = max(floor(2*R/dzStepTgt), 1)
zStep = 2*R/nZSamp
tight_layout()
draw()
show()

# <codecell>

n = 0
for z in np.linspace(-R+zStep/2, R-zStep/2, nZSamp):
    print "z:", z
    rhoMin = 0
    rhoMax = np.sqrt(R**2 - z**2)
    nRhoSamp = max(floor(rhoMax/rhoStepTgt), 1)
    rhoStep = rhoMax/nRhoSamp
    
    #-- Cylindrical wireframe
    polys = polVolDiffelVerts(rhoMax-rhoMax/2, 0, z,  rhoMax, 2*pi, zStep, R/10)
    diffDisk.set_verts(polys)
    

    for rho in np.linspace(rhoMin+rhoStep/2, rhoMax-rhoStep/2, nRhoSamp):
        nPhiSamp = max(floor(2*pi/(dsStepTgt/rho)),1)
        phiStep = 2*pi/nPhiSamp
        
        polys = polVolDiffelVerts(rho, 0, z,  rhoStep, 2*pi, zStep, zStep)
        diffTorus.set_verts(polys)

        for phi in np.linspace(phiStep/2, 2*pi-phiStep/2, nPhiSamp):
            polys = polVolDiffelVerts(rho, phi,z, rhoStep, phiStep, zStep, rhoStep/3)
            diffVolEl.set_verts(polys)

            (r_x0,r_y0) = pol2cart(rho, phi)
            r_z0 = z
            
            D_x = r_x1-r_x0
            D_y = r_y1-r_y0
            D_z = r_z1-r_z0
            
            D_rm3 = 10*Z**2*(D_x**2+D_y**2+D_z**2)**(-3/2)
            
            E_x1 = E_x0 + D_x*D_rm3
            E_y1 = E_y0 + D_y*D_rm3
            E_z1 = E_z0 + D_z*D_rm3

            ri_vec._verts3d = ([0,r_x0],[0,r_y0],[0,r_z0])
            ri_txt.set_position((n*r_x1+1,n*r_y1+1))
            draw()
            
            #rp_txt.set_3d_properties(z=r_z0)
            
            rp_vec._verts3d = ([r_x0,r_x1],[r_y0,r_y1], [r_z0,r_z1])
            #r_pt._verts3d = ([r_x0], [r_y0], [r_z0])
            Ei_vec._verts3d = ([E_x0,E_x1],[E_y0,E_y1],[E_z0,E_z1])
            #chunk.set_verts((chunk_x, chunk_y, chunk_z))
            plt.draw()
            if PERSP == "ISO":
                fig.savefig("frames/frame"+format(n, '04d')+"_iso.png")
            elif PERSP == "XSIDE":
                fig.savefig("frames/frame"+format(n, '04d')+"_xside.png")
            elif PERSP == "YSIDE":
                fig.savefig("frames/frame"+format(n, '04d')+"_yside.png")
            #plt.show()
            n += 1
            #time.sleep(0.1)
            #if n >= 50:
            #    raise Exception()

# <codecell>

close(2)
fig2 = plt.figure(2, figsize=(8,6))
fig2.clf()
ax2 = fig2.add_subplot(111, projection='3d')

n_angles = 30
n_radii = 10
min_radius = 0.0
radii = np.linspace(min_radius, 0.95, n_radii)

angles = np.linspace(0, 2*math.pi, n_angles, endpoint=False)
angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
angles[:, 1::2] += math.pi/n_angles

x = (radii*np.cos(angles)).flatten()
y = (radii*np.sin(angles)).flatten()
print x[0:10]
V = np.sqrt(x**2+y**2+0.1)
triang = Triangulation(x,y)
X, Y = np.meshgrid(x, y)

# # Mask off unwanted triangles.
# xmid = x[triang.triangles].mean(axis=1)
# ymid = y[triang.triangles].mean(axis=1)
# mask = np.where(xmid*xmid + ymid*ymid < min_radius*min_radius, 1, 0)
# triang.set_mask(mask)
ax2.plot3D(triang.x, triang.y,'b.') #, np.ones_like(triang.x), facecolors=V/max(V))
ax2.plot_surface(X,Y,np.sin(np.sqrt(X**2+Y**2)))
#ax2.tripcolor(triang) #, np.ones_like(triang.x), facecolors=V/max(V))
draw()
show()

# <codecell>

close(2)
fig2 = plt.figure(2, figsize=(8,6))
fig2.clf()
ax2 = fig2.add_subplot(111, projection='3d')
#ax.view_init(elev=1.1*Z, azim=25)
# b_x = [0,1,1,0]
# b_y = [0,0,1,1]
# b_z = [1,1,0,1]
# verts = [zip(b_x, b_y, b_z)]
#verts = [zip(x,y,np.ones_like(x))]
# for poly in polys:
#     ax2.add_collection3d(P3D([poly]))  (b_x,b_y,b_z,cmap=cm.coolwarm, linewidth=1, antialiased=False, color='b',

polys = polVolDiffelVerts(0.1,0,0, 0.2,2*pi,0.1, 0.05)
c = P3D(polys, linewidth=0.2, facecolor=(1,0.3,0.1), alpha=0.8)
ax2.add_collection3d(c)

draw()
show()

# <codecell>

polys = polVolDiffelVerts(0.2,0,0, 0.2,2*pi,0.1, 0.05)
c.set_verts(polys)
draw()

