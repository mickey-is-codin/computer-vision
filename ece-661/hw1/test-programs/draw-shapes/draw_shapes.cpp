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
    Mat input_img, output_img;

    // Set the input image and check for opening errors
    input_img = imread(img_path, CV_LOAD_IMAGE_COLOR);
    if (!input_img.data) {
        cout << "Failed to open specified image" << endl;
        return EXIT_FAILURE;
    }
    output_img = input_img.clone();

    // Get image resolution
    int im_x, im_y;
    im_x = output_img.cols;
    im_y = output_img.rows;

#ifdef DEBUG
    cout << "x size: " << im_x << "\ty size: " << im_y << endl;
#endif

    // Drawing
    // line(
    //     output_img,         // source
    //     (0,0),
    //     (),
    //     color,
    //     thickness
    // )

    // Create window and show image
    string window_title = "User Image: " + img_path;
    namedWindow(window_title);
    imshow(window_title, output_img);

    waitKey(0);

    return EXIT_SUCCESS;
}
