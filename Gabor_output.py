import numpy as np
from scipy import ndimage

def Gabor_output(inImg, bestWavelets, numFilters):

    # init
    input = inImg
    gaborResponses = []

    if type(input) != list:
        for filIdx in range(numFilters):
            filter = np.real(bestWavelets[filIdx])

            # normalize
            filter = filter / np.max(filter)
            gaborResponses.append(ndimage.convolve(input, filter, mode='nearest'))
    else:
        numImg = len(input)
        for imgIdx in range(numImg):
            for filIdx in range(numFilters):
                filter = np.real(bestWavelets[filIdx])

                # normalize
                filter = filter / np.max(filter)
                gaborResponses.append(ndimage.convolve(input[imgIdx], filter, mode='nearest'))

    return gaborResponses