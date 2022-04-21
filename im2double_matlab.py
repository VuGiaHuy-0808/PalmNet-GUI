import numpy as np

def im2double_matlab(im):
    info = np.iinfo(im.dtype)
    return im.astype(np.float) / info.max