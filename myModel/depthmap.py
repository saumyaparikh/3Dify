import cv2 
import numpy as np
from PIL import Image
def createdepthmap(left,right,img,lrsimilarity,tbsimilarity,fimage):
    depth_map = cv2.normalize(src=fimage, dst=fimage, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    depth_map = np.uint8(depth_map)
    if (tbsimilarity > lrsimilarity):
        depth_map = cv2.bitwise_not(depth_map)
    depth_image = Image.fromarray(depth_map, mode="L")
    colours_array  = np.array(left.resize(img.size)
                                .rotate(-90, expand=True)
                                .getdata()
                    ).reshape(img.size + (3,))
    return depth_image,colours_array