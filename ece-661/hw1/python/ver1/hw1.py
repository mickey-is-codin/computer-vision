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

    # Conduit Box
    # im_rect_pts = {
    #     'ul' : (182, 55),
    #     'ur' : (316, 96),
    #     'bl' : (154, 440),
    #     'br' : (296, 442)
    # }

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

    vec_a = np.cross(im_corner_vectors['bl'],im_corner_vectors['ul'])
    vec_b = np.cross(im_corner_vectors['bl'],im_corner_vectors['br'])
    vec_c = np.cross(im_corner_vectors['br'],im_corner_vectors['ur'])
    vec_d = np.cross(im_corner_vectors['ul'],im_corner_vectors['ur'])

    ver_van_pt = np.cross(vec_a, vec_c)
    hor_van_pt = np.cross(vec_b, vec_d)

    van_line = np.cross(ver_van_pt, hor_van_pt)
    print('Vanishing line: {}, shape: {}'.format(van_line, van_line.shape))

    # Manual
    homography = np.identity(len(van_line))
    homography[-1,:] = van_line

    h_inv = np.linalg.inv(homography)
    h_tran_inv = np.transpose(np.linalg.inv(homography))
    h_inv_tran = np.linalg.inv(np.transpose(homography))

    h_attempts = [homography, h_inv, h_tran_inv, h_inv_tran]

    shear_angle  = 15
    rotate_angle = 30

    tan_phi = np.tan(shear_angle)

    cos_theta = np.cos(rotate_angle)
    sin_theta = np.sin(rotate_angle)

    test_h = np.array([
        [1, tan_phi, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]).astype(np.float32)

    print('Test Homography: \n{}'.format(test_h))
    # print('Calculated Homography: \n{}'.format(homography))
    # print('Inverse: \n{}'.format(h_inv))
    # print('Inverse of Transpose: \n{}'.format(h_inv_tran))
    # print('Transpose of Inverse: \n{}'.format(h_tran_inv))

    # OpenCV Auto
    # Note: I believe this also removes the affine transformation
    image_points = np.float32([value[0:2] for key, value in im_corner_vectors.items()])
    world_points = np.float32([
        [400, 400],
        [400+400, 400],
        [400, 400+300],
        [400+400, 400+300]
    ])
    auto_perspective = cv2.getPerspectiveTransform(image_points, world_points)
    auto_homography = cv2.findHomography(image_points, world_points)

    translate_h = np.array([
        [1, 0, 100],
        [0, 1, 100],
        [0, 0, 1]
    ]).astype(np.float32)

    w = input_img.shape[1]
    h = input_img.shape[0]

    plot_im_corners(input_img, im_rect_pts)
    plot_im_edges(input_img, im_rect_pts)

    cv2.imshow('Input Image', input_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    output_shape = (w*2, h*2)
    output_img = cv2.warpPerspective(
        input_img,
        M=auto_perspective,
        dsize=output_shape
    )
    output_img = cv2.warpPerspective(
        output_img,
        M=translate_h,
        dsize=output_shape
    )

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
        'width':  input_img.shape[0],
        'height': input_img.shape[1],
        'channels': input_img.shape[2]
    }

    return image_info

if __name__ == '__main__':
    main()
