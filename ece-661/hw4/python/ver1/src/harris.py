import os
import sys
import time
import argparse

import cv2

import numpy as np

def main():

    print('Detecting corners in image...')
    args = read_cmd_args()

    print("Displaying {}".format(args.input_path))
    input_img = cv2.imread(args.input_path)
    output_img = input_img.copy()

    gray_input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

    dx, dy = compute_derivatives(gray_input_img)

    detect_corners(gray_input_img, dx, dy)

    show_results(gray_input_img, dx)

def detect_corners(img, dx, dy):

    pixel_count = 0
    for im_y in range(img.shape[0]):
        for im_x in range(img.shape[1]):

            #print("Getting C matrix for point ({},{}): {}".format(im_x, im_y, img[im_y, im_x]))
            c = np.zeros((2,2))

            for nb_y in range(-2,3):
                for nb_x in range(-2,3):
                    #print("Neighbor ({},{})".format(nb_x, nb_y))
                    #print("Indexing from derivative images at ({},{})".format(im_y + nb_y, im_x + nb_x))
                    if (im_y + nb_y > 0)            and \
                       (im_x + nb_x > 0)            and \
                       (im_y + nb_y < img.shape[0]) and \
                       (im_x + nb_x < img.shape[1]):
                        #print()
                        c[0,0] += np.square(dx[im_y + nb_y, im_x + nb_x])
                        c[0,1] += np.multiply(dx[im_y + nb_y, im_x + nb_x], dy[im_y + nb_y, im_x + nb_x])
                        c[1,0] += np.multiply(dx[im_y + nb_y, im_x + nb_x], dy[im_y + nb_y, im_x + nb_x])
                        c[1,1] += np.square(dx[im_y + nb_y, im_x + nb_x])

            #print(c)
            #return


def compute_derivatives(img):

    print("Input image: {}x{}".format(img.shape[1], img.shape[0]))

    der_x = cv2.Sobel(
        img,
        ddepth=-1,
        dx=1, dy=0,
        ksize=5
    )

    der_y = cv2.Sobel(
        img,
        ddepth=-1,
        dx=0, dy=1,
        ksize=5
    )

    return der_x, der_y

def show_results(input_img, output_img):
    cv2.imshow("Input Image", input_img)
    cv2.waitKey(0)

    cv2.imshow("Output Image", output_img)
    cv2.waitKey(0)

def read_cmd_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-path",
        help="path to input image",
        required=True
    )
    parser.add_argument(
        "-o", "--output-path",
        help="path to output image",
        required=True
    )

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    main()
