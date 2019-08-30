import cv2
import argparse

import numpy as np

def main():

    parser = argparse.ArgumentParser(description='Program to remove projective transformations from an image')
    parser.add_argument('-o', '--output', action='store', dest='output_path', required=True, help='input file')
    parser.add_argument('-i', '--input',  action='store', dest='input_path',  required=True, help='output file')
    args = parser.parse_args()

    print('\nRemoving distortion from {}...\n'.format(args.input_path))

    input_img = cv2.imread(args.input_path)
    image_info = get_image_info(input_img)
    print('Input image is a {}-channel {}x{} image'
        .format(image_info['channels'], image_info['width'], image_info['height']))

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

    print('\nCorner Points as Vectors: ')
    for k, v in im_corner_vectors.items():
        print('{}: {}, shape: {}'.format(k,v, v.shape))

    '''
             D
         -------->
        ^         ^
       A|         |C
        |         |
         -------->
             B
    '''

    input_im_array = np.array(input_img)
    output_im_array = np.zeros((2 * image_info['height'], 2 * image_info['width'], 3))
    print(input_im_array.shape, output_im_array.shape)

    vec_a = np.cross(im_corner_vectors['bl'],im_corner_vectors['ul'])
    vec_b = np.cross(im_corner_vectors['bl'],im_corner_vectors['br'])
    vec_c = np.cross(im_corner_vectors['br'],im_corner_vectors['ur'])
    vec_d = np.cross(im_corner_vectors['ul'],im_corner_vectors['ur'])
    print('Vector A: {}, shape: {}'.format(vec_a, vec_a.shape))
    print('Vector B: {}, shape: {}'.format(vec_b, vec_b.shape))
    print('Vector C: {}, shape: {}'.format(vec_c, vec_c.shape))
    print('Vector D: {}, shape: {}'.format(vec_d, vec_d.shape))

    ver_van_pt = np.cross(vec_a, vec_c)
    hor_van_pt = np.cross(vec_b, vec_d)

    van_line = np.cross(ver_van_pt, hor_van_pt)
    print('Vanishing line: {}, shape: {}'.format(van_line, van_line.shape))

    # Manual
    homography = np.identity(len(van_line))
    homography[-1,:] = van_line
    homography = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]).astype(np.float32)
    print('Original scene warped by homography: \n{}, shape: {}'.format(homography, homography.shape))

    h_inv = np.linalg.inv(homography)
    h_tran_inv = np.transpose(np.linalg.inv(homography))
    h_inv_tran = np.linalg.inv(np.transpose(homography))
    print('Inverse Homography: \n{}'.format(h_inv))
    print('Transposed Inverse Homography: \n{}'.format(h_tran_inv))

    h_attempts = [homography, h_inv, h_tran_inv, h_inv_tran]

    for y in range(image_info['height']):
        for x in range(image_info['width']):
            old_coords = [y, x, 1]
            new_coords = np.matmul(homography, old_coords)

            if x < 10 and y == 0:
                #print('New Coords: {}, Old Coords{}'.format((int(new_coords[0]), int(new_coords[1])),(y,x)))
                print('Setting location ({}, {}) on new image to {}'
                    .format(int(new_coords[0]), int(new_coords[1]), input_im_array[y,x]))

            output_im_array[int(new_coords[0]), int(new_coords[1])] = input_im_array[y,x]

    plot_im_corners(input_img, im_rect_pts)
    plot_im_edges(input_img, im_rect_pts)

    cv2.imshow('Input Image', input_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    output_img = output_im_array
    cv2.imshow('Output Image', output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

if __name__ == '__main__':
    main()
