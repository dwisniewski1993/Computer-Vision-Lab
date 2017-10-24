#include "stdafx.h"
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
using namespace cv;
using namespace std;
int main(int argc, char** argv)
{
	if (argc != 2)
	{
		cout << " Usage: display_image ImageToLoadAndDisplay" << endl;
		return -1;
	}
	Mat image;
	image = imread(argv[1], IMREAD_COLOR); // Read the file
	if (image.empty()) // Check for invalid input
	{
		cout << "Could not open or find the image" << std::endl;
		return -1;
	}
	//namedWindow("Display window", WINDOW_AUTOSIZE); // Create a window for display.
	//imshow("Display window", image); // Show our image inside it.
	
	Mat gray_image;
	cvtColor(image, gray_image, CV_BGR2GRAY);

	imwrite("../images/Gray_Image.jpg", gray_image);

	namedWindow("Lena", CV_WINDOW_AUTOSIZE);
	namedWindow("Gray Lena", CV_WINDOW_AUTOSIZE);

	imshow("Lena", image);
	imshow("Gray Lena", gray_image);

	//waitKey(0); // Wait for a keystroke in the window

	Mat bgr[3];
	split(image, bgr);

	imwrite("blue.png", bgr[0]); //blue channel
	imwrite("green.png", bgr[1]); //green channel
	imwrite("red.png", bgr[2]); //red channel

	namedWindow("Blue Lena", CV_WINDOW_AUTOSIZE);
	namedWindow("Green Lena", CV_WINDOW_AUTOSIZE);
	namedWindow("Red Lena", CV_WINDOW_AUTOSIZE);

	imshow("Blue Lena", bgr[0] );
	imshow("Green Lena", bgr[1]);
	imshow("Red Lena", bgr[2]);

	waitKey(0); // Wait for a keystroke in the window

	return 0;
}
