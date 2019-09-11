import cv2
import argparse
from tqdm import tqdm

import numpy as np

def main():

    args = get_cmd_args()

    print('\nRemoving projective distortion from {} using OpenCV builtin methods...\n'
        .format(args.input_path))

    input_img = cv2.imread(args.input_path)
    image_info = get_image_info(input_img, args.verbose)

    im_rect_pts = {
        'ul' : (450, 55),
        'ur' : (760, 175),
        'bl' : (430, 430),
        'br' : (748, 440)
    }

    im_corner_vectors = {
        'ul' : np.transpose(np.array([im_rect_pts['ul'][0], im_rect_pts['ul'][1],  1])),
        'ur' : np.transpose(np.array([im_rect_pts['ur'][0], im_rect_pts['ur'][1],  1])),
        'bl' : np.transpose(np.array([im_rect_pts['bl'][0], im_rect_pts['bl'][1], 1])),
        'br' : np.transpose(np.array([im_rect_pts['br'][0], im_rect_pts['br'][1], 1]))
    }

    if args.verbose:
        print('\nUser-defined rectangle corner homogenous coordinates: ')
        for k, v in im_corner_vectors.items():
            print(k, v)

    new_origin = [500, 400]
    x_scale = 500
    y_scale = 300

    image_points = np.float32([value[0:2] for key, value in im_corner_vectors.items()])

    world_points = np.float32([
        new_origin,
        [new_origin[0]+x_scale, new_origin[1]],
        [new_origin[0], new_origin[1]+y_scale],
        [new_origin[0]+x_scale, new_origin[1]+y_scale]
    ])

    print('\nCalculating inverse homography...')

    auto_perspective = cv2.getPerspectiveTransform(image_points, world_points)

    plot_im_corners(input_img, im_rect_pts)
    plot_im_edges(input_img, im_rect_pts)

    w = input_img.shape[1]
    h = input_img.shape[0]

    print('\nApplying inverse homography to input image...')

    output_shape = (w*2, h*2)
    output_img = cv2.warpPerspective(
        input_img,
        M=auto_perspective,
        dsize=output_shape
    )

    cv2.imwrite(args.output_path, output_img)
    print('\nAll done!')

def plot_im_edges(input_img, rect_points):

    line_1 = cv2.line(
        input_img,
        pt1=rect_points['bl'],
        pt2=rect_points['ul'],
        color=(0,0,255),
        thickness=2
    )

    line_2 = cv2.line(
        input_img,
        pt1=rect_points['bl'],
        pt2=rect_points['br'],
        color=(0,0,255),
        thickness=2
    )

def plot_im_corners(input_img, rect_points):

    cv2.circle(
        input_img,
        center=rect_points['ul'],
        radius=3,
        color=(255,0,0),
        thickness=3
    )

    cv2.circle(
        input_img,
        center=rect_points['ur'],
        radius=3,
        color=(255,0,0),
        thickness=3
    )

    cv2.circle(
        input_img,
        center=rect_points['bl'],
        radius=3,
        color=(255,0,0),
        thickness=3
    )

    cv2.circle(
        input_img,
        center=rect_points['br'],
        radius=3,
        color=(255,0,0),
        thickness=3
    )

def get_image_info(input_img, verbose=False):

    image_info = {
        'width':  input_img.shape[0],
        'height': input_img.shape[1],
        'channels': input_img.shape[2]
    }

    if verbose:
        print('Input is a {}-channel {}x{} image'
            .format(image_info['channels'], image_info['width'], image_info['height']))

    return image_info

def get_cmd_args():

    parser = argparse.ArgumentParser(
        description='Program to remove projective transformations from an image'
    )
    parser.add_argument(
        '-o', '--output',
        action='store',
        dest='output_path',
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-i', '--input',
        action='store',
        dest='input_path',
        required=True,
        help='output file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        help='verbose output'
    )
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    main()
