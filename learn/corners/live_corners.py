import sys

import numpy as np
import cv2

def main():
    print("Beginning program...")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Operate on frame here


        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
