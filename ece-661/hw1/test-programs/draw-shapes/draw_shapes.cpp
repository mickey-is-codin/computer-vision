#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <cstdlib>

using namespace std;
using namespace cv;

int main(int argc, char ** argv) {

    if (argc != 2) {
        cout << "Usage: make-bw image" << endl;
        return EXIT_FAILURE;
    }

    cout << "\nConverting image...";

#ifdef DEBUG
    cout << "=Compiled in debug mode=" << endl;
#endif

    // Get the input image from command line argument
    string img_path = argv[1];
    cout << img_path << endl;

    // Declare images
    Mat input_img;

    // Set the input image and check for opening errors
    input_img = imread(img_path, CV_LOAD_IMAGE_COLOR);
    if (!input_img.data) {
        cout << "Failed to open specified image" << endl;
        return EXIT_FAILURE;
    }

    // Create window and show image
    string window_title = "User Image: " + img_path;
    namedWindow(window_title);
    imshow(window_title, input_img);

    waitKey(0);

    return EXIT_SUCCESS;
}
