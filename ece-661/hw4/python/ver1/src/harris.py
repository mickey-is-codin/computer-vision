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
    gray_input_img = gray_input_img / np.max(gray_input_img)

    dx, dy = compute_derivatives(gray_input_img)

    detect_corners(gray_input_img, output_img, dx, dy)

    show_results(gray_input_img, output_img)

def detect_corners(input_img, output_img, dx, dy):

    corner_thresh = 200_000
    k = 0.04

    u = 2
    v = 2

    ratios = np.array([])
    passed_ratios = np.array([])

    pixel_count = 0
    for im_y in range(input_img.shape[0]):
        for im_x in range(input_img.shape[1]):

            e = np.zeros((2,2))
            m = np.zeros((2,2))

            window_sum = np.sum(input_img[im_y-v:im_y+v, im_x-u:im_x+u])

            m[0,0] = dx[im_y,im_x]
            m[0,1] = dx[im_y,im_x] * dy[im_y,im_x]
            m[1,0] = m[0,1]
            m[1,1] = dy[im_y, im_x]

            m = m * window_sum

            # e = np.matmul(np.array([u, v]), m)
            # e = np.matmul(e, np.array(np.transpose([u, v])))

            if np.sum(m) > 0:
                det_m = (m[0,0] * m[1,1]) - (m[0,1] * m[1,0])
                tr_m  = m[0,0] + m[1,1]

                r = np.abs(det_m - k * (tr_m**2))
                ratios = np.append(ratios, r)

                if r > corner_thresh:
                    passed_ratios = np.append(passed_ratios, r)

                    # Draw circle here instead
                    output_img[im_y, im_x] = [0,0,255]

            pixel_count += 1

    print(np.min(ratios))
    print(np.max(ratios))
    print(np.mean(ratios))
    print(np.std(ratios))
    print(np.percentile(ratios, 99))
    print('Num corners: {}'.format(len(passed_ratios)))

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
