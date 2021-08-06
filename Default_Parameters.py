import numpy as np
from scipy.spatial.transform import Rotation as SciRot


def parameters():
    translation = np.array([[3.7484, 0.0, 0.6601699999999999]])
    rotation = SciRot.from_quat([0.5941767906169857, -0.5878843193897473, 0.3873184109007999, -0.3890121040340926]).as_matrix()
    height = 966
    width = 1280
    size = [width,height]
    cx_offset = 3.942
    cy_offset = -3.093
    principle_point = [cx_offset,cy_offset]
    aspect_ratio = 1.0
    coefficients = [339.749, -31.988, 48.275, -7.201]

    return rotation, translation, coefficients, size, principle_point, aspect_ratio


