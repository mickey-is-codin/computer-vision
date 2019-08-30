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
        'ul' : (182, 55),
        'ur' : (316, 96),
        'bl' : (154, 440),
        'br' : (296, 442)
    }

    im_corner_vectors = {
        'ul' : np.transpose(np.array([182, 55,  1])),
        'ur' : np.transpose(np.array([316, 96,  1])),
        'bl' : np.transpose(np.array([154, 440, 1])),
        'br' : np.transpose(np.array([296, 442, 1]))
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
    # homography = np.identity(len(van_line))
    # homography[-1,:] = van_line
    # print('Homography: \n{}'.format(homography))

    # OpenCV Auto
    image_points = np.float32([value[0:2] for key, value in im_corner_vectors.items()])
    world_points = np.float32([[0,0], [300,0], [0,300], [300,300]])
    homography = cv2.getPerspectiveTransform(image_points, world_points)

    output_shape = (input_img.shape[0], input_img.shape[1])
    output_img = cv2.warpPerspective(
        input_img,
        M=homography,
        dsize=(300,300)
    )

    plot_im_corners(input_img, im_rect_pts)
    plot_im_edges(input_img, im_rect_pts)

    cv2.imshow('Input Image', input_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
