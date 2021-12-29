# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 10:46:23 2018

@author: wxfou
"""

import imageio
import os
from os.path import join as osj

def create_gif( image_list, gif_name ):
    frames = []
    
    for image_name in image_list:
        frames.append( imageio.imread( image_name) )
    imageio.mimsave( gif_name, frames, 'GIF', duration = 0.5 )
    
    return

def main(imgPath, saveGifFileName):
    '''
    '''
    image_list = []
    for rt, subdirs, files in os.walk( imgPath ):
        for file in files:    
            image_list.append(  osj(rt, file) )
    
    create_gif( image_list, saveGifName )

if __name__=='__main__':
    imgPath = 'D:/project/PyProject/clouddata/data_cloud_pred_mask'
    saveGifName = 'D:/project/PyProject/clouddata/pred_femur_tibia.gif'
    main( imgPath, saveGifName)
        
        
        
        