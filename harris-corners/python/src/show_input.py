import os
import sys
import time
import argparse

import cv2

import numpy as np

def main():

    print('Showing input image')
    args = read_cmd_args()

    print("Displaying {}".format(args.input_path))
    input_img = cv2.imread(args.input_path)

    cv2.imshow("Input Image", input_img)
    cv2.waitKey(0)

def read_cmd_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-path",
        help="input image to display",
        required=True
    )

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    main()
