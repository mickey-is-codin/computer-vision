import os
import sys
import time
import cv2

import numpy as np

def main():
    print("Beginning sample blur program...")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        blur = cv2.GaussianBlur(
            frame,
            ksize=(5,5),
            sigmaX=1,
            sigmaY=1
        )
        cv2.imshow('frame', blur)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
