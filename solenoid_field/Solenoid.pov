//******************************************************************************************
//* Magnetic Field of a Solenoid, copyright by Paul Nylander, bugman123.com, 5/17/06
//* runtime: 1 minute
//******************************************************************************************

// Modified slightly by J.L. Lanfranchi for demonstrating solenoid fields

//#declare mu0=1.25663706144e-6; #declare n=6; #declare R=0.01; #declare dL=(4/3)*R; #declare r=R/4;
#declare mu0=1.25663706144e-6; #declare numcoils=1+floor(clock*300); #declare R=0.01; #declare r=R/8; #declare dL=2*r; 
camera{location <13.65,0,16.25>*R look_at 0.4*R*x up -y right x*image_width/image_height sky -y angle 25}
light_source{<0,0,8*R>,1}

//Solenoid
#include "golds.inc"
#declare begin=1; #declare x1=(0.05-numcoils/2)*dL;
#while(x1<=(numcoils/2-0.0)*dL)
 #declare theta=2*pi*(x1/dL+numcoils/2)-pi; #declare p2=<x1,R*sin(theta),-R*cos(theta)>;
 #if(mod(theta+pi,2*pi)>0.4*pi & mod(theta+pi,2*pi)<1.6*pi)
 	sphere{p2,r texture{T_Gold_5A}}
 	//cylinder{p1,p2,r texture{T_Gold_1A}}
 	//#if(!begin)
 	//    cylinder{p1,p2,r texture{T_Gold_1A}}
 	//#end
 #end
 #declare begin=0; #declare p1=p2; #declare x1=x1+0.005*dL;
#end

//Electromagnetic Field
#declare Sqr=function(X) {X*X};
#declare sign=function(i1) {1-2*floor(2*mod((i1-1)/2,numcoils)/numcoils)}; // i1<n1?1:-1
#declare I=function(i1) {sign(i1)}; // current
#declare xcoil=function(i1) {dL*(mod(i1-1,numcoils)+0.5*floor(2*mod((i1-1)/2,numcoils)/numcoils)-0.5*(numcoils-0.5))};
#declare B=function{(mu0/(2*pi))*sqrt( // magnetic field magnitude
 Sqr(sum(i1,1,2*numcoils,I(i1)*(y-sign(i1)*R)/(Sqr(x-xcoil(i1))+Sqr(y-sign(i1)*R))))+
 Sqr(sum(i1,1,2*numcoils,I(i1)*(x-xcoil(i1))/(Sqr(x-xcoil(i1))+Sqr(y-sign(i1)*R))))
)}
//#declare contours=function{(2+cos(0.06*pi*(sum(i1,1,2*numcoils,I(i1)/sqrt(Sqr(x-xcoil(i1))+Sqr(y-sign(i1)*R))))))/3} // magnetic field line contours
//#declare contours=function{(2+cos(0.002*pi*(sum(i1,1,2*numcoils,I(i1)/sqrt(Sqr(x-xcoil(i1))+Sqr(y-sign(i1)*R))))))/3} // magnetic field line contours
//plane{<0,0,1>,0
// //pigment{function{min(1,max(0,12000*B(x,y,0)*contours(x,y,0)))} color_map{
// //pigment{function{min(1,max(0,3600*B(x,y,0)*contours(x,y,0)))} color_map{
// pigment{function{min(1,max(0,24000*B(x,y,0)*contours(x,y,0)))} color_map{
//  [0 rgbt <0,0,1,1>] [0.25 rgbt <0,0,1,0.75>] [0.5 rgbt <1/3,0,1,0.75>] [0.75 rgbt <2/3,0.5,1,0.75>] [1 rgbt <1,1,0,0.75>] 
//  [0.9 rgbt <0,0,1,.75>] [0.99 rgbt <1,0,0,0.75>] [0.999 rgbt <0,1,0,0.75>] [0.9999 rgbt <1,0,1,.75>] [1 rgbt <1,1,1,.75>]
// }}
// //pigment{function{min(1,max(0,3600*B(x,y,0)*contours(x,y,0)))} color_map{
////	 [0.0 color rgbt <0,0,0,1>] [0.000 color rgbt <0,0,0,1>] [0.333 color rgbt <0,0,.5,.75>] [0.333 color rgbt <0,0,.5,.75>] [0.666 color rgbt <0,0,1,.75>] [0.666 color rgbt <.5,.5,0>] [1.000 color rgbt <1,1,0>] [1.000 color rgbt <1,1,0>] [1.000 color rgbt <1,1,1,.75>] } }
// finish{ambient 2.25 reflection 0 diffuse 0 specular 0}
//}

#declare contours=function{(2+cos(0.01*pi*(sum(i1,1,2*numcoils,I(i1)/sqrt(Sqr(x-xcoil(i1))+Sqr(y-sign(i1)*R))))))/4} // magnetic field line contours
plane{<0,0,1>,0
 pigment{function{min(1,max(0,6000*B(x,y,0)*contours(x,y,0)))} color_map{
  [0 rgbt <0,0,1,1>] [0.25 rgbt <0,0,1,0.9>] [0.5 rgbt <1/3,0,1,0.9>] [0.75 rgbt <2/3,0.5,1,0.9>] [1 rgbt <1,1,1,0.9>]
 }}
 finish{ambient 8.25 reflection 0.02 diffuse 0.1 specular 0.001}
 //finish{ambient 0.25 reflection 0 diffuse 0 specular 0}
}
