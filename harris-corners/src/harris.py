import os
import sys
import time
import argparse

import cv2

import numpy as np

from tqdm import tqdm

def main():

    print('Detecting corners in image...')
    args = read_cmd_args()

    print("Displaying {}".format(args.input_path))
    input_img = cv2.imread(args.input_path)
    output_img = input_img.copy()

    gray_input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    gray_input_img = np.float32(gray_input_img)
    #gray_input_img = gray_input_img / np.max(gray_input_img)

    dx, dy = compute_derivatives(gray_input_img)

    detect_corners(gray_input_img, output_img, dx, dy)

    show_results(input_img, output_img)

def detect_corners(input_img, output_img, dx, dy):

    harris_mask = np.zeros_like(input_img)

    dx_2  = np.square(dx)
    dx_dy = np.multiply(dx, dy)
    dy_2  = np.square(dy)

    k = 0.04

    block_size = 2

    for im_y in tqdm(range(block_size, input_img.shape[0])):
        for im_x in range(block_size, input_img.shape[1]):

            m = np.zeros((2,2))

            #window_sum = np.sum(input_img[im_y-block_size:im_y+block_size, im_x-block_size:im_x+block_size])
            #window_sum = block_size*block_size
            #window = np.ones((block_size,block_size))

            #print(dx_2[im_y-v:im_y+v+1,im_x-u:im_x+u+1])

            m[0,0] = np.sum(dx_2[im_y-block_size:im_y+block_size+1,im_x-block_size:im_x+block_size+1])
            m[0,1] = np.sum(dx_dy[im_y-block_size:im_y+block_size+1,im_x-block_size:im_x+block_size+1])
            m[1,0] = np.sum(m[0,1])
            m[1,1] = np.sum(dy_2[im_y-block_size:im_y+block_size+1,im_x-block_size:im_x+block_size+1])

            det_m = (m[0,0] * m[1,1]) - (m[0,1] * m[1,0])
            tr_m  = m[0,0] + m[1,1]

            r = np.abs(det_m - k * (tr_m**2))

            harris_mask[im_y, im_x] = r

    harris_mask = cv2.dilate(harris_mask, None)

    corner_thresh = np.percentile(harris_mask, 97)
    corner_mask = harris_mask > corner_thresh
    output_img[corner_mask] = [0,0,255]

def compute_derivatives(img):

    print("Input image: {}x{}".format(img.shape[1], img.shape[0]))

    der_x = cv2.Sobel(
        img,
        ddepth=-1,
        dx=1, dy=0,
        ksize=3
    )

    der_y = cv2.Sobel(
        img,
        ddepth=-1,
        dx=0, dy=1,
        ksize=3
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
