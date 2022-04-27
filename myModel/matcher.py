import cv2
import numpy as np
def lrmatcher(window_size,limage,rimage):
    lmatcher = cv2.StereoSGBM_create(
                minDisparity=0,
                numDisparities=16,
                blockSize=5,
                P1=8 * 3 * window_size ** 2,
                P2=32 * 3 * window_size ** 2,
            )         
    rmatcher = cv2.ximgproc.createRightMatcher(lmatcher)
    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=lmatcher)
    wls_filter.setLambda(80000)
    wls_filter.setSigmaColor(1.2)
    left_disparity  = lmatcher.compute(limage, rimage)
    right_disparity = rmatcher.compute(rimage, limage)
    left_disparity  = np.int16(left_disparity)
    right_disparity = np.int16(right_disparity)
    imagefiltered  = wls_filter.filter(left_disparity, limage, None, right_disparity)
    return imagefiltered