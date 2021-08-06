import numpy as np


def Fisheye_ProjectionMatrix(translation, rotation):
    projection_matrix = np.eye(4)
    projection_matrix[0:3, 3] = translation
    projection_matrix[0:3, 0:3] = rotation
    inv_projection_matrix = np.linalg.inv(projection_matrix)

    return projection_matrix, inv_projection_matrix