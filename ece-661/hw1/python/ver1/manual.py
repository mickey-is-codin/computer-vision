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

    plot_im_corners(input_img, im_rect_pts)
    plot_im_edges(input_img, im_rect_pts)

    cv2.imshow('Input Image', input_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Correspondences
    m1 = np.zeros((len(image_points)*2, len(image_points)*2))
    row = 0
    for i in range(len(image_points)):
        m1[row:row+2, :] = build_p(image_points[i], world_points[i])
        row += 2
    print('Shape of M1 Matrix: {}'.format(m1.shape))

    m2 = np.zeros(len(image_points) * 2)
    for ix, pt in enumerate(world_points):
        m2[ix]   = pt[0]
        m2[ix+4] = pt[1]
    print(m2)

    #m1_inv_t = np.linalg.inv( np.matmul( np.transpose(m1),m1 ) )
    #m1_m2 = np.matmul( np.transpose(m1),m2 )
    #print(m1_inv_t.shape)
    #print(m1_m2.shape)
    homography = np.matmul( np.linalg.inv( np.matmul(np.transpose(m1),m1) ),( np.matmul(np.transpose(m1),m2) ))
    homography = np.append(homography, 1)
    homography = homography.reshape(3,3)

    w = input_img.shape[1]
    h = input_img.shape[0]

    output_shape = (w*2, h*2)
    output_img = cv2.warpPerspective(
        input_img,
        M=homography,
        dsize=output_shape
    )

    print('Calculated Homography: \n{}, shape: {}'.format(homography, homography.shape))

    #output_img = output_im_array
    cv2.imshow('Output Image', output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def build_p(im_pt, wo_pt):
    p = np.array([
        [im_pt[0], im_pt[1], 1,        0,        0, 0, -im_pt[0]*wo_pt[0], -im_pt[1]*wo_pt[0]],
        [       0,        0, 0, im_pt[0], im_pt[1], 1, -im_pt[0]*wo_pt[1], -im_pt[1]*wo_pt[1]]
    ]).astype(np.float32)

    return p

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
