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

    // Get the input image from command line argument
    string img_path = argv[1];
    cout << img_path << endl;

#ifdef DEBUG
    cout << "=Compiled in debug mode=" << endl;
#endif

    // Declare images
    Mat input_img;

    // Set the input image and check for opening errors
    input_img = imread(img_path, CV_LOAD_IMAGE_COLOR);
    if (!input_img.data) {
        cout << "Failed to open specified image" << endl;
        return EXIT_FAILURE;
    }



    return EXIT_SUCCESS;
}
