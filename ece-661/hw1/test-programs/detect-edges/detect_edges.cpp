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
    Mat input_img, gray_img, sobel_mask, edge_img;

    // Set the input image and check for opening errors
    input_img = imread(img_path, CV_LOAD_IMAGE_COLOR);
    if (!input_img.data) {
        cout << "Failed to open specified image" << endl;
        return EXIT_FAILURE;
    }

    // Convert image to grayscale
    cvtColor(input_img, gray_img, COLOR_BGR2GRAY);

    // Create the sobel mask.
    Sobel(
        gray_img,       // source image
        sobel_mask,     // destination image
        CV_32F,         // output channels?
        1, 0,           // xorder, yorder
        7               // kernel size
    );

    double min_value, max_value, scale;
    minMaxLoc(sobel_mask, &min_value, &max_value);
    scale = 255.0 / (max_value - min_value);
#ifdef DEBUG
    cout << "min intensity: " << min_value << "\tmax value: " << max_value << endl;
#endif

    // Change the range of the image
    sobel_mask.convertTo(
        edge_img,               // Destination
        CV_8U,                  // Datatype = 8 bit unsigned int
        scale,                  // Scale factor (alpha)
        -min_value * scale      // Delta added to scaled value
    );

    // Create window and show image
    string window_title = "User Image: " + img_path;
    namedWindow(window_title);
    imshow(window_title, edge_img);

    waitKey(0);

    return EXIT_SUCCESS;
}
