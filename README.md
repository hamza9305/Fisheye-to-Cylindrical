# Fisheye-to-Cylindrical

The project takes in a Fisheye image, and projects it to a Cylindrical panorama

 

![conversion](https://github.com/hamza9305/Fisheye-to-Cylindrical/blob/main/data/conversion.gif)

 

## Description

The script read a fisheye image, projects it to 3D space using the intrinsics and extrinsics parameters and then maps it to a cylindrical panorama using the projection matrix of a cylindrical projection. For this project particularly I have used the [WoodScape](https://github.com/valeoai/WoodScape) dataset which is one of the first publically avaialble fisheye dataset. The dataset also provides the intrinsics and extrinsics parameters of the camera which are used for the project. These parameters can be changed if a different imageset is used and similar results can be obtained.

 

I have also given a detailed explanation on how to change these parameters for a new dataset in ths Scripts section.  

 

## Requirements

- python 3

```bash

conda create -n Fisheye2Cylindrical python=3.6

```

```bash

conda activate Fisheye2Cylindrical

```

- numpy

```bash

conda install -c conda-forge opencv

```

- numpy

```bash

conda install -c anaconda numpy

```

- matplotlib

```bash

conda install -c conda-forge matplotlib

```

- scipy

```bash

conda install -c anaconda scipy

```

- argparse

```bash

conda install -c conda-forge argparse

```

 

Alternatively you can also set the environment using the requirments.txt file by the following command

```bash

pip install -r requirments

```

 

## Scripts

The projects contains the following scripts.

- Fisheye2Cylindrical.py

This is the main python script that converts the fisheye image to cylindrical panorama. The paramaters to run this script are as follows.

  - --img_dir: directory of the image

  - --use_default: use default intrinsics and extrinsics as set in the [Default_Parameters.py](https://github.com/hamza9305/Fisheye-to-Cylindrical/blob/main/Default_Parameters.py)

  - --json_config: default=False, whether to use json file for intrinsic and extrinsic

  - --json_path: path to Json file

  - --out_dir: directory location for output image

  - --vis: default=Fale, set True if you want to visualize

 

- Default_arguements.py

This script contains the default arguments that are needed to run the [Fisheye2Cylindrical.py](https://github.com/hamza9305/Fisheye-to-Cylindrical/blob/main/Fisheye2Cylindrical.py) script. Modifications can be done as per the need and relevant fucntionality can be obtained.

 

- Default_Parameters.py

This script contains the default intrinsic and extrinsic parameters of the WoodScape dataset which can be changed if a different dataset is used. It contains the following parameters

  - translation

  - rotation

  - height

  - width

  - cx_offset

  - cy_offset

  - aspect_ratio

  - distortion coefficients

 

- Json_file.py

This file reads the intrinsics and extrinsics parameters of how it has been designed for the WoodScape dataset. Naturally for any other format, a new script can be wriiten and integrated with the project.

 

- Cylindrical_Projection.py

It contains the projection matrix of the cylindrical panorama

 

- Fisheye_Projection.py

It contains the projection matrix of the Fisheye
