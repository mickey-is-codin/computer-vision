#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <cstdlib>

using namespace std;
using namespace cv;

int main(int argc, char ** argv) {

    if (argc != 3) {
        cout << "Usage: make-bw input-image output-image" << endl;
        return EXIT_FAILURE;
    }

    cout << "\nConverting image...";

    // Get the input image from command line argument
    string input_path  = argv[1];
    string output_path = argv[2];
    cout << input_path << " into " << output_path << endl;

#ifdef DEBUG
    cout << "=Compiled in debug mode=" << endl;
#endif

    // Declare images
    Mat input_img, output_img;

    // Set the input image and check for opening errors
    input_img = imread(input_path, CV_LOAD_IMAGE_COLOR);
    if (!input_img.data) {
        cout << "Failed to open specified image" << endl;
        return EXIT_FAILURE;
    }


    return EXIT_SUCCESS;
}
