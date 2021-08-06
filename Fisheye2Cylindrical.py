import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from Default_arguements import default_argument_parser
import os
from Default_Parameters import parameters
from Json_file import read_json
from Cylindrical_Projection import Cylindrical_ProjectionMatrix
from Fisheye_Projection import Fisheye_ProjectionMatrix



class Fisheye2Cylinderical:
    def __init__(self,size,fish_projection_mat,cyc_projection_mat, principle_point, aspect_ratio,distortion_coefficients):
        self._pose = np.asarray(fish_projection_mat[0], dtype=float)
        self._inv_pose = np.asarray(fish_projection_mat[1], dtype=float)
        self._pose_cyc = np.asarray(cyc_projection_mat[0], dtype=float)
        self._inv_pose_cyc = np.asarray(cyc_projection_mat[1], dtype=float)
        self._size = np.array([size[0], size[1]], dtype=int)
        self._principle_point = 0.5 * self._size + np.array([principle_point[0], principle_point[1]], dtype=float) - 0.5
        self._aspect_ratio = np.array([1, aspect_ratio], dtype=float)
        self.focal_length = distortion_coefficients[0]
        self.coefficients = np.asarray(distortion_coefficients)
        self.power = np.array([np.arange(start=1, stop=len(self.coefficients) + 1)]).T

    def project_3d_to_2d_Image(self,cam_points):
        cam_points = np.matmul(cam_points, self._inv_pose.T)
        chi = np.sqrt(cam_points.T[0] * cam_points.T[0] + cam_points.T[1] * cam_points.T[1])
        theta = np.arctan2(chi, cam_points.T[2])
        rho = self.theta_to_rho(theta)
        lens_points = np.divide(rho, chi, where=(chi != 0))[:, np.newaxis] * cam_points[:, 0:2]
        screen_points = (lens_points * self._aspect_ratio) + self._principle_point
        return screen_points

    def theta_to_rho(self,theta):
        return np.dot(self.coefficients, np.power(np.array([theta]), self.power))

    def project_2d_to_3d_Cylindrical(self, image_points: np.ndarray):

        outs = np.zeros((image_points.shape[0], 3))
        theta = image_points.T[0] / self.focal_length
        outs.T[0] = self.focal_length * np.sin(theta)
        outs.T[1] = image_points.T[1]
        outs.T[2] = self.focal_length * np.cos(theta)
        return outs

    def create_img_projection_maps(self, destination_cam_size):
        width = destination_cam_size[0]
        height = destination_cam_size[1]
        u_map = np.zeros((height, width, 1), dtype=np.float32)
        v_map = np.zeros((height, width, 1), dtype=np.float32)

        destination_points_b = np.arange(height)

        for u_px in range(width):
            destination_points_a = np.ones(height) * u_px
            destination_points = np.vstack((destination_points_a, destination_points_b)).T

            lens_points = (destination_points - self._principle_point) / self._aspect_ratio
            camera_points = self.project_2d_to_3d_Cylindrical(lens_points)
            camera_points = np.concatenate((np.array(camera_points), np.ones((camera_points.shape[0], 1))), axis=1)
            world_points = np.matmul(camera_points, self._pose_cyc.T)

            source_points = self.project_3d_to_2d_Image(world_points)
            u_map.T[0][u_px] = source_points.T[0]
            v_map.T[0][u_px] = source_points.T[1]
        map1, map2 = cv.convertMaps(u_map, v_map, dstmap1type=cv.CV_16SC2, nninterpolation=False)
        return map1, map2

def main():
    args = default_argument_parser().parse_args()
    print(args)

    params = []
    if args.use_default:
        params = parameters()

    if args.json_config:
        if args.json_path is None:
            print("Path to Json file not specified")
            exit(0)
        else:
            params = read_json(args.json_path)

    if args.img_dir is None:
        print("Enter the image path")
        exit(0)

    fisheye_image = cv.imread(args.img_dir)

    if args.out_dir is None:
        print("Specify output directory")
        exit(0)
    output_dir = args.out_dir + "\\" + 'cyc_' + os.path.basename(args.img_dir)

    rotation = params[0]
    translation = params[1]
    coefficients = params[2]
    size = [int(a) for a in params[3]]
    principle_point = params[4]
    aspect_ratio = params[5]

    cyc_projection_mat = Cylindrical_ProjectionMatrix(translation,rotation)
    fish_projection_mat = Fisheye_ProjectionMatrix(translation,rotation)

    cam = Fisheye2Cylinderical(size = size,
                       fish_projection_mat = fish_projection_mat,
                       cyc_projection_mat = cyc_projection_mat,
                       principle_point = principle_point,
                       aspect_ratio = aspect_ratio,
                       distortion_coefficients = coefficients)


    map1,map2 = cam.create_img_projection_maps(size)
    cylindrical_image = cv.remap(fisheye_image, map1, map2, cv.INTER_CUBIC)

    if args.vis:
        plt.imshow(cv.cvtColor(fisheye_image, cv.COLOR_BGR2RGB))
        plt.show()
        plt.imshow(cv.cvtColor(cylindrical_image, cv.COLOR_BGR2RGB))
        plt.show()

    cv.imwrite(output_dir, cylindrical_image)


if __name__ == '__main__':
    main()

