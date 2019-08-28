import numpy as np
import cv2

def main():

    img = cv2.imread('images/notre_dame.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray, None)

    img = cv2.drawKeypoints(gray, kp, img)

    cv2.imwrite('images/sift_keypoints.jpg', img)

if __name__ == '__main__':
    main()
