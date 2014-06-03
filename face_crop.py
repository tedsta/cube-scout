#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Philipp Wagner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the author nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys, math
import os
from cv2 import *
import numpy as np

def Distance(p1,p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx*dx+dy*dy)

def rotate_image(image, angle, resample=INTER_CUBIC):
    image_center = tuple(np.array(image.shape)/2)
    rot_mat = getRotationMatrix2D(image_center,angle,1.0)
    result = warpAffine(image, rot_mat, image.shape,flags=resample)
    return result

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=INTER_CUBIC):
    if (scale is None) and (center is None):
        return rotate_image(image, angle, resample)
    nx,ny = x,y = center
    sx=sy=1.0
    if new_center:
        (nx,ny) = new_center
    if scale:
        (sx,sy) = (scale, scale)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    a = cosine/sx
    b = sine/sx
    c = x-nx*a-ny*b
    d = -sine/sy
    e = cosine/sy
    f = y-nx*d-ny*e
    
    size_x, size_y, _ = image.shape
    mat = np.array([[a, b, c],\
                    [d, e, f]])
    return warpAffine(image, mat, (size_x, size_y), flags=resample)

def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (130,130)):
    # calculate offsets in original image
    offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
    offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
    # get the direction
    eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
    # calc rotation angle in radians
    rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
    # distance between them
    dist = Distance(eye_left, eye_right)
    # calculate the reference eye-width
    reference = dest_sz[0] - 2.0*offset_h
    # scale factor
    scale = float(dist)/float(reference)
    # rotate original around the left eye
    image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
    # crop the rotated image
    crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
    crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
    image = image[int(crop_xy[1]):int(crop_xy[1]+crop_size[1]), int(crop_xy[0]):int(crop_xy[0]+crop_size[0])]
    # resize it
    image = resize(image, dest_sz)
    return image

def readFileNames(fn_csv):
    try:
        inFile = open(fn_csv)
    except:
        raise IOError('There is no file named '+fn_csv+' in current directory.')
        return False

    picPath = []
    picIndex = []

    for line in inFile.readlines():
        if line != '':
            fields = line.rstrip().split(';')
            picPath.append(fields[0])
            picIndex.append(int(fields[1]))

    return (picPath, picIndex)

###########################################################

# Mouse callback
eye_step = 0 
eye_positions = [None, None]
def mouse_callback(event, x, y, flags, param):
    global eye_step
    global eye_positions

    if event == EVENT_LBUTTONDOWN:
        eye_positions[eye_step] = (x, y)
        eye_step += 1

def main():
    global eye_step
    global eye_positions

    namedWindow("image")
    setMouseCallback("image", mouse_callback)

    # Load images
    [images, indexes]=readFileNames(sys.argv[1])
    if not os.path.exists("modified"):
        os.makedirs("modified")

    # Crop images
    for img in images:
        image = imread(img)
        print(img)
        eye_step = 0
        eye_positions = [None, None]
        while eye_step != 2:
            key = waitKey(20)
            if key == 27:
                break
            imshow("image", image)
        if eye_positions[0] and eye_positions[1]:
            img_path = img.rstrip().split('/')
            cropped_image = CropFace(image, eye_left=eye_positions[0], eye_right=eye_positions[1], offset_pct=(0.2,0.2), dest_sz=(200,200))
            imwrite("modified/"+img_path[2]+'/'+img_path[3], cropped_image)
        #CropFace(image, eye_left=(252,364), eye_right=(420,366), offset_pct=(0.1,0.1), dest_sz=(200,200)).save("modified/"+img.rstrip().split('/')[2]+"_10_10_200_200.jpg")
        #CropFace(image, eye_left=(252,364), eye_right=(420,366), offset_pct=(0.2,0.2), dest_sz=(200,200)).save("modified/"+img.rstrip().split('/')[2]+"_20_20_200_200.jpg")
        #CropFace(image, eye_left=(252,364), eye_right=(420,366), offset_pct=(0.3,0.3), dest_sz=(200,200)).save("modified/"+img.rstrip().split('/')[2]+"_30_30_200_200.jpg")
        #CropFace(image, eye_left=(252,364), eye_right=(420,366), offset_pct=(0.2,0.2)).save("modified/"+img.rstrip().split('/')[2]+"_20_20_70_70.jpg")


###########################################################

if __name__ == "__main__":
    main()
