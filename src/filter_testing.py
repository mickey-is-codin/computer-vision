import os
import sys
import time
import cv2

import numpy as np

def main():
    print("Beginning filter testing program...")

    filter_choice = 7

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if filter_choice == 0:
            filtered_frame = cv2.GaussianBlur(
                frame,
                ksize=(5,5),
                sigmaX=1,
                sigmaY=5
            )
        elif filter_choice == 1:
            filtered_frame = cv2.blur(
                frame,
                ksize=(5,5)
            )
        elif filter_choice == 2:
            filtered_frame = cv2.boxFilter(
                frame,
                ddepth=-1,
                ksize=(5,5)
            )
        elif filter_choice == 3:
            filtered_frame = cv2.Sobel(
                frame,
                ddepth=-1,
                ksize=5,
                dx=0,
                dy=1
            )
        elif filter_choice == 4:
            filtered_frame = cv2.Scharr(
                frame,
                ddepth=-1,
                dx=1,
                dy=0
            )
        elif filter_choice == 5:
            filtered_frame = cv2.pyrMeanShiftFiltering(
                frame,
                sp=21,
                sr=51
            )
        elif filter_choice == 6:
            filtered_frame = cv2.medianBlur(
                frame,
                ksize=21
            )
        elif filter_choice == 7:
            filtered_frame = cv2.dilate(
                frame,
                kernel=cv2.getStructuringElement(
                    shape=cv2.MORPH_ELLIPSE,
                    ksize=(5,5)
                )
            )
        elif filter_choice == 8:
            filtered_frame = cv2.erode(
                frame,
                kernel=cv2.getStructuringElement(
                    shape=cv2.MORPH_RECT,
                    ksize=(5,5)
                )
            )

        cv2.imshow('frame', filtered_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
