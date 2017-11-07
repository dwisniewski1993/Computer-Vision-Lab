#include "stdafx.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;

/**
* function main
*/
int main(int argc, char** argv)
{
	Mat src = imread("lena.jpg");
	imshow("Original Picture", src);
	
	//Rotacja
	Mat dst;

	double angle = 90;  // or 270
	Size src_sz = src.size();
	Size dst_sz(src_sz.height, src_sz.width);

	int len = std::max(src.cols, src.rows);
	Point2f center(len / 2., len / 2.);
	Mat rot_mat = getRotationMatrix2D(center, angle, 1.0);
	warpAffine(src, dst, rot_mat, dst_sz);

	imshow("Rotated Picture", dst);

	waitKey(0);

	//Image Pyramid - Zoom
	Mat tmp;
	tmp = src;
	dst = tmp;

	/// Loop
	while (true)
	{
		int c;
		c = waitKey(10);

		if ((char)c == 'e')
		{
			break;
		}
		if ((char)c == 'u')
		{
			pyrUp(tmp, dst, Size(tmp.cols * 2, tmp.rows * 2));
			printf("** Zoom In: Image x 2 \n");
		}
		else if ((char)c == 'd')
		{
			pyrDown(tmp, dst, Size(tmp.cols / 2, tmp.rows / 2));
			printf("** Zoom Out: Image / 2 \n");
		}

		imshow("Zomed", dst);
		tmp = dst;
	}

	waitKey(0);

	//Grey scale



}

