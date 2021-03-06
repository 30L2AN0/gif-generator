# gif-generator

## Description

A gif generator with interpolation and user interface

The frames are drawn and positioned on a timeline by the user

## Setup

All code is implemented in python

Libraries needed :
- user interface : tkinter
- image management : PIL
- gif generation : glob, os
- interpolation : PIL, numpy, os, matplotlib

`gif_generator.py` launchs the user interface and fabrics `output.gif` with the images in `gif/`

`interpolation.py` computs an intermediate image `intermed.png` with the ones in `interpolation/`

`iterative_closest` pics `imageA.png` in `ITC/`, translates and rotates it to create a virtual `imageB` and then finds back automatically the translation and rotation matrix from the two pictures positions

## Results

Automatically generated transition image between a square and a circle
<div align='center'>
  <img src='gallery/fixed_interpolation/image0.png' height="225px">
  <img src='gallery/fixed_interpolation/rond_carre.png' height="225px">
  <img src='gallery/fixed_interpolation/image1.png' height="225px">
</div>

Interpolated gif with only 4 drawn frames

<div align='center'>
  <img src='gallery/dancing_square.gif' height='500px'>
</div>

## To do

- Improve the interpolation when a drawing contains significantly more black pixels than the other
- Enable elliptic transitions between frames
- Allow the user to link segments to improve the interpolation
