import math
import numpy as np
import cv2

def adjustFormat(im):
    # Compute image size
    # Image size must be power of 2
    closPow2 = int(math.pow(2, math.floor(math.log2(im.shape[0]))))
    imageSize = (closPow2, closPow2)

    # Back to rgb
    im = (im * 255).round().astype(np.uint8)
    # Cast
    im = im.astype(np.float64)
    # Resize image, must be power of 2
    im = cv2.resize(im, imageSize, interpolation=cv2.INTER_CUBIC)
    # Subtract mean
    im = im - cv2.mean(im)[0]

    return im