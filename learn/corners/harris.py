import sys

import numpy as np
import cv2

def main():

    if len(sys.argv) == 1:
        filename = 'images/chess.png'
    elif len(sys.argv) == 2:
        filename = sys.argv[1]

    print('Detecting corners for {}...\n'.format(filename))

    img = cv2.imread(filename)
    result = img

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    print('Shape of input image: {}\n'.format(gray.shape))

    harris_mask = cv2.cornerHarris(
        src=gray,
        blockSize=2,
        ksize=3,
        k=0.04
    )

    harris_mask = cv2.dilate(harris_mask,None)
    result[harris_mask > 0.01 * harris_mask.max()] = [0, 0, 255]

    print('Mask Analysis:')
    print('Type of result of Harris algorithm:  {}'.format(type(harris_mask)))
    print('Shape of result of Harris algorithm: {}'.format(harris_mask.shape))

    cv2.imshow('Result of Harris Algorithm', result)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
