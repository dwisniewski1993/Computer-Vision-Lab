#include "stdafx.h"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>

using namespace cv;

/// Global variables
Mat src, dst, erosion_dst, dilation_dst;

int morph_elem = 0;
int morph_size = 0;
int morph_operator = 0;
int const max_operator = 4;
int const max_elem = 2;
int const max_kernel_size = 21;

int erosion_elem = 0;
int erosion_size = 0;
int dilation_elem = 0;
int dilation_size = 0;


char* window_name = "Morphology Transformations Demo";

/** Function Headers */
void Morphology_Operations(int, void*);
void Erosion(int, void*);
void Dilation(int, void*);

/** @function main */
int main(int argc, char** argv)
{
	/// Load an image
	src = imread(argv[1]);

	if (!src.data)
	{
		return -1;
	}

	/// Create window
	namedWindow(window_name, CV_WINDOW_AUTOSIZE);
	namedWindow("Erosion Demo", CV_WINDOW_AUTOSIZE);
	namedWindow("Dilation Demo", CV_WINDOW_AUTOSIZE);
	cvMoveWindow("Dilation Demo", src.cols, 0);

	/// Create Erosion Trackbar
	createTrackbar("Element:\n 0: Rect \n 1: Cross \n 2: Ellipse", "Erosion Demo",
		&erosion_elem, max_elem,
		Erosion);

	createTrackbar("Kernel size:\n 2n +1", "Erosion Demo",
		&erosion_size, max_kernel_size,
		Erosion);

	/// Create Dilation Trackbar
	createTrackbar("Element:\n 0: Rect \n 1: Cross \n 2: Ellipse", "Dilation Demo",
		&dilation_elem, max_elem,
		Dilation);

	createTrackbar("Kernel size:\n 2n +1", "Dilation Demo",
		&dilation_size, max_kernel_size,
		Dilation);

	/// Create Trackbar to select Morphology operation
	createTrackbar("Operator:\n 0: Opening - 1: Closing \n 2: Gradient - 3: Top Hat \n 4: Black Hat", window_name, &morph_operator, max_operator, Morphology_Operations);

	/// Create Trackbar to select kernel type
	createTrackbar("Element:\n 0: Rect - 1: Cross - 2: Ellipse", window_name,
		&morph_elem, max_elem,
		Morphology_Operations);

	/// Create Trackbar to choose kernel size
	createTrackbar("Kernel size:\n 2n +1", window_name,
		&morph_size, max_kernel_size,
		Morphology_Operations);

	/// Default start
	Morphology_Operations(0, 0);
	Erosion(0, 0);
	Dilation(0, 0);

	waitKey(0);
	return 0;
}

/**
* @function Morphology_Operations
*/
void Morphology_Operations(int, void*)
{
	// Since MORPH_X : 2,3,4,5 and 6
	int operation = morph_operator + 2;

	Mat element = getStructuringElement(morph_elem, Size(2 * morph_size + 1, 2 * morph_size + 1), Point(morph_size, morph_size));

	/// Apply the specified morphology operation
	morphologyEx(src, dst, operation, element);
	imshow(window_name, dst);
}

void Erosion(int, void*)
{
	int erosion_type;
	if (erosion_elem == 0) { erosion_type = MORPH_RECT; }
	else if (erosion_elem == 1) { erosion_type = MORPH_CROSS; }
	else if (erosion_elem == 2) { erosion_type = MORPH_ELLIPSE; }

	Mat element = getStructuringElement(erosion_type,
		Size(2 * erosion_size + 1, 2 * erosion_size + 1),
		Point(erosion_size, erosion_size));

	/// Apply the erosion operation
	erode(src, erosion_dst, element);
	imshow("Erosion Demo", erosion_dst);
}

/** @function Dilation */
void Dilation(int, void*)
{
	int dilation_type;
	if (dilation_elem == 0) { dilation_type = MORPH_RECT; }
	else if (dilation_elem == 1) { dilation_type = MORPH_CROSS; }
	else if (dilation_elem == 2) { dilation_type = MORPH_ELLIPSE; }

	Mat element = getStructuringElement(dilation_type,
		Size(2 * dilation_size + 1, 2 * dilation_size + 1),
		Point(dilation_size, dilation_size));
	/// Apply the dilation operation
	dilate(src, dilation_dst, element);
	imshow("Dilation Demo", dilation_dst);
}