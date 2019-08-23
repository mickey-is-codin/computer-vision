import cv2

import numpy as np
import matplotlib.pyplot as plt

def main():
    train_data = np.random.randint(0, 100, (25,2)).astype(np.float32)
    responses = np.random.randint(0, 2, (25,1)).astype(np.float32)

    red = train_data[responses.ravel()==0]
    plt.scatter(red[:,0], red[:,1], 80, 'r', '^')

    blue = train_data[responses.ravel()==1]
    plt.scatter(blue[:,0], blue[:,1], 80, 'b', 's')

    plt.show()

if __name__ == '__main__':
    main()
