from django.shortcuts import render
import pandas as pd
import numpy as np
import cv2
import argparse
from . import matcher
from . import depthmap
from pyntcloud import PyntCloud   
from PIL import Image
class Mesh:
    def createmesh(self,filename):
        img = Image.open(filename).convert('RGB')
        w, h = img.size
        r  = img.crop( (0,       0, w/2, h))
        l   = img.crop( (w/2, 0, w,   h))
        t    = img.crop( (0,        0, w, h/2))
        b = img.crop( (0, h/2, w,   h))
        try:
            l_r_same = self.mse(np.array(r), np.array(l))
            t_b_same = self.mse(np.array(t),   np.array(b))
        except:
            return 0
        if (t_b_same < l_r_same):
            l  = b
            r = t
        image_l  = np.array(l) 
        image_r = np.array(r) 
        window_size = 15
        filtered_image  = matcher.lrmatcher(window_size,image_l,image_r)
        depth_image,coloursarray=depthmap.createdepthmap(l,r,img,l_r_same,t_b_same,filtered_image)
        indicesarray = np.moveaxis(np.indices(img.size), 0, 2)
        image_Array    = np.dstack((indicesarray, coloursarray)).reshape((-1,5))
        df = pd.DataFrame(image_Array, columns=["x", "y", "red","green","blue"])
        depths_array = np.array(depth_image.resize(img.size)
                                        .rotate(-90, expand=True)
                                        .getdata())     
        df.insert(loc=2, column='z', value=depths_array)
        df[['red','green','blue']] = df[['red','green','blue']].astype(np.uint)
        df[['x','y','z']] = df[['x','y','z']].astype(float)
        df['z'] = df['z']*5
        cloud = PyntCloud(df)
        cloud.to_file(filename+".ply", also_save=["mesh","points"],as_text=True)
        return 1
    def mse(self,imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err