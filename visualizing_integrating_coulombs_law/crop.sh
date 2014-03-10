#!/bin/bash

#mkdir frames/cropped

#for fname in `ls frame*_*side.png | sed 's/\.png//g'`;do
#	echo $fname
#	convert ${fname}.png -crop 450x550+190+125 frames/cropped/${fname}_crop.png
#done

#for fname in `ls frame*_iso.png | sed 's/\.png//g'`;do
#	echo ${fname}
#	convert ${fname}.png -crop 500x550+175+25 frames/cropped/${fname}_crop.png
#done

#for fname in `ls frame*_iso.png | sed 's/_iso\.png//g'`;do 
#	echo $fname
#	convert frames/cropped/${fname}_iso_crop.png frames/cropped/${fname}_xside_crop.png frames/cropped/${fname}_yside_crop.png +append frames/cropped/${fname}_cat.png
#	#convert frames/cropped/${fname}_iso_crop.png frames/cropped/${fname}_xside_crop.png +append frames/cropped/${fname}_cat.png
#done

#mencoder mf://frames/cropped/frame*_cat.png -lavcopts vcodec=msmpeg4v2:vbitrate=1200 -mf type=png:fps=20 -ovc lavc -o visual_coulomb_integral.avi
mencoder mf://frames/cropped/frame*_cat.png -lavcopts vcodec=msmpeg4v2:vbitrate=1000 -mf type=png:fps=20 -ovc lavc -o visual_coulomb_integral.avi


