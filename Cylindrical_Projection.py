import numpy as np
from scipy.spatial.transform import Rotation as SciRot


def Cylindrical_ProjectionMatrix(translation, rotation):

    projection_matrix = np.eye(4)
    projection_matrix[0:3, 3] = translation
    rot_zxz = SciRot.from_matrix(rotation).as_euler('zxz')
    rot_zxz = np.round(rot_zxz / (np.pi / 2)) * (np.pi / 2)
    rotation_cyc = SciRot.from_euler(angles=rot_zxz, seq='zxz').as_matrix()

    projection_matrix[0:3, 0:3] = rotation_cyc
    inv_projection_matrix = np.linalg.inv(projection_matrix)
    return projection_matrix, inv_projection_matrix


