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

    detect_corners(gray_input_img, output_img, dx, dy)

    show_results(gray_input_img, output_img)

def detect_corners(input_img, output_img, dx, dy):

    corner_thresh = 0.3

    #ratios = np.array([])

    pixel_count = 0
    for im_y in range(input_img.shape[0]):
        for im_x in range(input_img.shape[1]):

            c = np.zeros((2,2))

            c[0,0] = np.sum(np.square(dx[im_y-2:im_y+2, im_x-2:im_y+2]))
            c[0,1] = np.sum(np.multiply(dx[im_y-2:im_y+2, im_x-2:im_y+2], dy[im_y-2:im_y+2, im_x-2:im_y+2]))
            c[1,0] = c[0,1]
            c[1,1] = np.sum(np.square(dy[im_y-2:im_y+2, im_x-2:im_y+2]))

            det_c   = (c[0,0] * c[1,1]) - (c[0,1] * c[1,0])
            trace_c = c[0,0] + c[1,1]

            if np.sum(c) > 0:
                ratio = np.abs(det_c / (trace_c ** 2))
                #ratios = np.append(ratios, ratio)

                if (ratio > corner_thresh):
                    output_img[im_y, im_x] = [0, 0, 255]

            pixel_count += 1

    # print(np.mean(ratios))
    # print(np.max(ratios))
    # print(np.min(ratios))
    # print(np.percentile(ratios, 99))
    # print(np.std(ratios))


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
