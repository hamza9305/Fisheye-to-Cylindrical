import argparse


def default_argument_parser():
    parser = argparse.ArgumentParser(description="Fisheye to Cylindrical Projection")
    parser.add_argument("--img_dir", help = 'directory of the image')
    parser.add_argument("--use_default", default = False, help="use default intrinsics and extrinsics")
    parser.add_argument("--json_config",default=False, help="whether to use json file for intrinsic and extrinsic")
    parser.add_argument("--json_path", help="path to Json file")
    parser.add_argument("--out_dir",help = 'directory location for output image')
    parser.add_argument("--vis", default=False, help = 'set True if you want to visualize')
    parser.add_argument(
        "--machine-rank", type=int, default=0, help="the rank of this machine (unique per machine)"
    )
    return parser