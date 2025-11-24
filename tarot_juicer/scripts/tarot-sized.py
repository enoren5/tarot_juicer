""" This script fills a use case where I needed batch / mogrify functionality
but with the ability to use image magick's quality, sampling and strip to batch
crop and downscale tarot card images to be used for thumbnails"""

import argparse
from pathlib import Path
import subprocess

def resize(file, out, geometry):
    command = f'convert {str(file)} -resize {geometry} -format jpeg {out.name}/{file.name}'
    subprocess.run(command.split())
    print(command)

def crop(file, out, geometry, quality):
    command = f'convert {str(file)} -gravity Center -interlace Plane -sampling-factor 4:2:0 -crop {geometry} -format jpeg -quality {quality}  -strip {out.name}/{file.name}'
    subprocess.run(command.split())
    print(command)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='use image magicks convert to batch resize tarot cards')
    parser.add_argument('in_dir', type=str, help='input directory - process all jpegs inside')
    parser.add_argument('out_dir', type=str, help='output directory - place processed images')
    args = parser.parse_args()
    groups = [Path(args.in_dir) / f'group0{group}' for group in range(1,4)]
    bad_resolution = ['group02', 'group01']
    out_dir = Path(args.out_dir)
    tmp_dir = Path('tmp')
    resize_geometry = '240x360!'
    crop_geometry = '220x360:+10:+0'
    for group in groups:
        for file in group.glob('*.jpg'):
            resize(file, tmp_dir, resize_geometry)
            crop(tmp_dir / file.name, out_dir, crop_geometry, 85)
            
        