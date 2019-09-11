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
    int img_x, img_y;
    img_x = output_img.cols;
    img_y = output_img.rows;

#ifdef DEBUG
    cout << "x size: " << img_x << "\ty size: " << img_y << endl;
#endif

    // Define cv2::Point2i's for start and end of line
    Point2i start(0,0);
    Point2i end(100,100);

    // Drawing

    // Create a line
    line(
        output_img,         // source
        start,              // Start (Point2i)
        end,                // End (Point2i)
        Scalar(0,255,0),    // Color
        2                   // Line thickness
    );

    circle(
        output_img,
        Point2i(int(img_x/2), int(img_y/2)),
        5,
        Scalar(0,255,0),
        2
    );

    // Create window and show image
    string window_title = "User Image: " + img_path;
    namedWindow(window_title);
    imshow(window_title, output_img);

    return EXIT_SUCCESS;
}
