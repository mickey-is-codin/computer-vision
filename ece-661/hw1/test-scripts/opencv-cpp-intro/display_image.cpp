#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <cstdlib>

using namespace std;
using namespace cv;

int main(int argc, char ** argv) {

    if (argc != 2) {
        cout << "Usage: image-display image" << endl;
        return EXIT_FAILURE;
    }

    cout << "\nDisplaying image...";

#ifdef DEBUG
    cout << "=Compiled in debug mode=" << endl;
#endif

    string img_path = argv[1];
    cout << img_path << endl;

    Mat input_img;
    input_img = imread(img_path, CV_LOAD_IMAGE_COLOR);

    if (!input_img.data) {
        cout << "Failed to open specified image" << endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
