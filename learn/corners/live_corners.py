import sys

import numpy as np
import cv2

def main():
    print("Beginning program...")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Harris Algorithm Logic
        result = frame

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)

        harris_mask = cv2.cornerHarris(
            src=gray,
            blockSize=3,
            ksize=5,
            k=0.04
        )

        harris_mask = cv2.dilate(harris_mask,None)
        result[harris_mask > 0.01 * harris_mask.max()] = [0, 0, 255]

        cv2.imshow('Harris Algorithm Corners', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
