import os
import sys
import time
import argparse

import cv2

import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt

def main():

    print('Detecting corners in image...')
    args = read_cmd_args()

    print("Displaying {}".format(args.input_path))
    input_img = cv2.imread(args.input_path)
    output_img = input_img.copy()

    gray_input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    gray_input_img_32 = np.float32(gray_input_img)

    harris_mask = cv2.cornerHarris(
        gray_input_img_32,
        blockSize=2,
        ksize=3,
        k=0.04
    )

    harris_mask = cv2.dilate(harris_mask, None)
    output_img[harris_mask > 0.01 * harris_mask.max()] = [0,0,255]

    cv2.imwrite(args.output_path, output_img)

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
