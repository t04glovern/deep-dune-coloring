#!/bin/sh

## Convert PDF to images
mkdir dune
convert -verbose -colorspace RGB -resize 1000 -interlace none -density 300 -quality 80 dune-coloring-book-remaster.pdf[0-25] dune/image.png

## Split images into pages
cd dune
mkdir pages
for file in `ls *.png`; do
	convert -crop 50%x100% +repage `echo $file` `echo pages/$file | sed 's/\.png$/\.%01d.png/'`
done