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

    im_ul_crnr = (135,90)
    im_ur_crnr = (400, 100)
    im_bl_crnr = ()
    im_br_crnr = ()

    cv2.circle(
        input_img,
        center=im_ul_crnr,
        radius=5,
        color=(255,0,0),
        thickness=2
    )

    cv2.circle(
        input_img,
        center=im_ur_crnr,
        radius=5,
        color=(255,0,0),
        thickness=2
    )

    cv2.imshow('Input Image', input_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_image_info(input_img):

    image_info = {
        'width':  input_img.shape[0],
        'height': input_img.shape[1],
        'channels': input_img.shape[2]
    }

    return image_info

if __name__ == '__main__':
    main()
