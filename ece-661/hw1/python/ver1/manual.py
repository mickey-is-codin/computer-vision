import cv2
import argparse

import numpy as np

def main():

    args = get_cmd_args()

    print('\nRemoving distortion from {}...\n'.format(args.input_path))

    input_img = cv2.imread(args.input_path)
    image_info = get_image_info(input_img)
    print('Input image is a {}-channel {}x{} image'
        .format(image_info['channels'], image_info['width'], image_info['height']))

    input_img_copy = input_img

    im_rect_pts = {
        'ul' : (450, 55),
        'ur' : (760, 175),
        'bl' : (430, 430),
        'br' : (748, 440)
    }

    im_corner_vectors = {
        'ul' : np.transpose(np.array([im_rect_pts['ul'][0], im_rect_pts['ul'][1],  1])),
        'ur' : np.transpose(np.array([im_rect_pts['ur'][0], im_rect_pts['ur'][1],  1])),
        'bl' : np.transpose(np.array([im_rect_pts['bl'][0], im_rect_pts['bl'][1],  1])),
        'br' : np.transpose(np.array([im_rect_pts['br'][0], im_rect_pts['br'][1],  1]))
    }

    new_origin = [500, 400]
    world_x_scale = 500
    world_y_scale = 300

    image_points = np.float32([value[0:2] for key, value in im_corner_vectors.items()])

    world_points = np.float32([
        new_origin,
        [new_origin[0] + world_x_scale, new_origin[1]],
        [new_origin[0], new_origin[1] + world_y_scale],
        [new_origin[0] + world_x_scale, new_origin[1] + world_y_scale]
    ])

    print('\nCorner Points as Vectors: ')
    for k, v in im_corner_vectors.items():
        print('{}: {}, shape: {}'.format(k,v, v.shape))

    plot_im_corners(input_img, im_rect_pts)
    plot_im_edges(input_img, im_rect_pts)

    A, B = get_A_B(world_points, image_points)

    homography = np.linalg.solve(A, B)
    homography = np.append(homography, 1)
    homography = homography.reshape(3,3)
    print('H: ', homography)

    h_inv = np.linalg.inv(homography)

    w = input_img.shape[1]
    h = input_img.shape[0]

    output_shape = (w*2, h*2, 3)
    output_img = np.zeros(output_shape).astype(np.uint8)

    for y in range(image_info['height']):
        for x in range(image_info['width']):

            in_pixel = input_img_copy[y, x]

            old_coords = np.transpose(np.array([x, y, 1]).astype(np.float32))
            new_coords = np.matmul(h_inv, old_coords)

            new_x = int(new_coords[0] / new_coords[2])
            new_y = int(new_coords[1] / new_coords[2])

            output_img[new_y, new_x] = in_pixel

    cv2.imwrite(args.output_path, output_img)

def get_A_B(wo_pts, im_pts):

    A = np.zeros((len(wo_pts) * 2, len(wo_pts) * 2))
    B = np.zeros((len(wo_pts) * 2, 1))

    crnr_ix = 0
    for row_ix in np.arange(0, A.shape[0], 2):

        print(row_ix)
        A[row_ix][0] = wo_pts[crnr_ix][0]
        A[row_ix][1] = wo_pts[crnr_ix][1]
        A[row_ix][2] = 1
        A[row_ix][3] = 0
        A[row_ix][4] = 0
        A[row_ix][5] = 0
        A[row_ix][6] = -im_pts[crnr_ix][0]*wo_pts[crnr_ix][0]
        A[row_ix][7] = -im_pts[crnr_ix][0]*wo_pts[crnr_ix][1]

        A[row_ix+1][0] = 0
        A[row_ix+1][1] = 0
        A[row_ix+1][2] = 0
        A[row_ix+1][3] = wo_pts[crnr_ix][0]
        A[row_ix+1][4] = wo_pts[crnr_ix][1]
        A[row_ix+1][5] = 1
        A[row_ix+1][6] = -im_pts[crnr_ix][1]*wo_pts[crnr_ix][0]
        A[row_ix+1][7] = -im_pts[crnr_ix][1]*wo_pts[crnr_ix][1]

        B[row_ix]   = im_pts[crnr_ix][0]
        B[row_ix+1] = im_pts[crnr_ix][1]

        crnr_ix += 1

    print('A shape: ', A.shape)
    print('B shape: ', B.shape)
    print('A: ', A)
    print('B: ', B)
    return A, B


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


def get_image_info(input_img):

    image_info = {
        'height':  input_img.shape[0],
        'width': input_img.shape[1],
        'channels': input_img.shape[2]
    }

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
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    main()
