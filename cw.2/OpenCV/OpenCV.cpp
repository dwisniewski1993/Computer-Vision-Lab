#include "stdafx.h"
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
using namespace cv;
using namespace std;


void Sharpen(const Mat& myImage, Mat& Result)
{
	CV_Assert(myImage.depth() == CV_8U);  // accept only uchar images

	Result.create(myImage.size(), myImage.type());
	const int nChannels = myImage.channels();

	for (int j = 1; j < myImage.rows - 1; ++j)
	{
		const uchar* previous = myImage.ptr<uchar>(j - 1);
		const uchar* current = myImage.ptr<uchar>(j);
		const uchar* next = myImage.ptr<uchar>(j + 1);

		uchar* output = Result.ptr<uchar>(j);

		for (int i = nChannels; i < nChannels * (myImage.cols - 1); ++i)
		{
			*output++ = saturate_cast<uchar>(5 * current[i]
				- current[i - nChannels] - current[i + nChannels] - previous[i] - next[i]);
		}
	}

	Result.row(0).setTo(Scalar(0));
	Result.row(Result.rows - 1).setTo(Scalar(0));
	Result.col(0).setTo(Scalar(0));
	Result.col(Result.cols - 1).setTo(Scalar(0));
}

int main(int argc, char** argv)
{
	//HELLO LENA CW1
	if (argc != 2)
	{
		cout << " Usage: display_image ImageToLoadAndDisplay" << endl;
		return -1;
	}
	Mat image;
	image = imread(argv[1], IMREAD_COLOR);
	if (image.empty())
	{
		cout << "Could not open or find the image" << std::endl;
		return -1;
	}
	
	//GREY LENA CW2 tutorial
	Mat gray_image;
	cvtColor(image, gray_image, CV_BGR2GRAY);

	imwrite("../images/Gray_Image.jpg", gray_image);

	namedWindow("Lena", CV_WINDOW_AUTOSIZE);
	namedWindow("Gray Lena", CV_WINDOW_AUTOSIZE);

	imshow("Lena", image);
	imshow("Gray Lena", gray_image);

	waitKey(0);

	// RBG LENA CW2 zad 5
	Mat bgr[3];
	Mat sharper;
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

	//SHARPER LENA CW2 zad 6b

	Sharpen(image, sharper);

	imshow("Sharper", sharper);
	waitKey(0);

	//AVG LENA CW2 zad6a

	Mat kernel, dst;
	Point anchor;
	double delta;
	int ddepth;
	int kernel_size;
	char* window_name = "Rozmywana Lena";

	int c;

	/// Initialize arguments for the filter
	anchor = Point(-1, -1);
	delta = 0;
	ddepth = -1;

	/// Loop - Will filter the image with different kernel sizes each 0.5 seconds
	int ind = 0;
	while (true)
	{
		c = waitKey(500);
		/// Press 'ESC' to exit the program
		if ((char)c == 27)
		{
			break;
		}

		/// Update kernel size for a normalized box filter
		kernel_size = 3 + 2 * (ind % 5);
		kernel = Mat::ones(kernel_size, kernel_size, CV_32F) / (float)(kernel_size*kernel_size);

		/// Apply filter
		filter2D(image, dst, ddepth, kernel, anchor, delta, BORDER_DEFAULT);
		imshow(window_name, dst);
		ind++;
		waitKey(0); // Ka¿da spacja to wiêksze rozmycie... do pewnego momentu
	}

	waitKey(0);



	return 0;
}
