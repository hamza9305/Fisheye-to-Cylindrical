import json
from scipy.spatial.transform import Rotation as SciRot


def read_json(path):
    with open(path) as f:
        config = json.load(f)

    intrinsic = config['intrinsic']

    rotation = SciRot.from_quat(config['extrinsic']['quaternion']).as_matrix()
    translation = config['extrinsic']['translation']
    coefficients = [intrinsic['k1'], intrinsic['k2'], intrinsic['k3'], intrinsic['k4']]
    size = [intrinsic['width'], intrinsic['height']]
    principle_point = (intrinsic['cx_offset'], intrinsic['cy_offset'])
    aspect_ratio = intrinsic['aspect_ratio']

    return rotation, translation, coefficients, size, principle_point, aspect_ratio
