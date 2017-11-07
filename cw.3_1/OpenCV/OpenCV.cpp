#include "stdafx.h"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace std;
using namespace cv;

/// Global Variables
int DELAY_CAPTION = 1500;
int DELAY_BLUR = 100;
int MAX_KERNEL_LENGTH = 31;

Mat src; Mat dst;
char window_name[] = "Filter Demo 1";

/// Function headers
int display_caption(char* caption);
int display_dst(int delay);

/**
* function main
*/
int main(int argc, char** argv)
{
	namedWindow(window_name, CV_WINDOW_AUTOSIZE);

	/// Load the source image
	src = imread("lena.jpg", 1);

	imshow("Original Picture", src);

	/// Median blur - wygl¹da³ na dzia³aj¹cy najlepiej
	if (display_caption("Median Blur") != 0) { return 0; }

	for (int i = 1; i < MAX_KERNEL_LENGTH; i = i + 2)
	{
		medianBlur(src, dst, i);
		if (display_dst(DELAY_BLUR) != 0) { return 0; }
	}

	/// Wait until user press a key
	display_caption("End: Press a key!");

	waitKey(0);
	return 0;
}

int display_caption(char* caption)
{
	dst = Mat::zeros(src.size(), src.type());
	putText(dst, caption,
		Point(src.cols / 4, src.rows / 2),
		CV_FONT_HERSHEY_COMPLEX, 1, Scalar(255, 255, 255));

	imshow(window_name, dst);
	int c = waitKey(DELAY_CAPTION);
	if (c >= 0) { return -1; }
	return 0;
}

int display_dst(int delay)
{
	imshow(window_name, dst);
	int c = waitKey(delay);
	if (c >= 0) { return -1; }
	return 0;
}