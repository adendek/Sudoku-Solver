# Sudoku-Solver
This program is designed to solve the [Sudoku puzzle](https://en.wikipedia.org/wiki/Sudoku), taken from the camera.
It uses [openCV](https://opencv.org/) library for image processing, [Keras](https://en.wikipedia.org/wiki/Keras) for image recognition and it uses [Backtracking](https://en.wikipedia.org/wiki/Backtracking) algorithm for saving it.

<img src="https://media1.giphy.com/media/QAuUc245sZHO/giphy.gif" width="200" height="200" />

Table of contents
=================
<!--ts-->
* [Sudoku-Solver](#sudoku-solver)
* [Table of contents](#table-of-contents)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Quick start](#quick-start)
* [How does it work?](#how-does-it-work)
    * [Extracting Sudoku field](#extracting-sudoku-field)
        * [Image pre-processing](#image-pre-processing)
        * [Finding the biggest blob](#finding-the-biggest-blob)
        * [Detecting lines](#detecting-lines)
        * [Result](#result)
    * [Extracting digits](#extracting-digits)
* [Tests](#tests)
* [Authors](#authors)
<!--te-->
    
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### 1. Python

You need Python 3.4 or later to run Sudoku-Solver. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, Mint and Debian you can install Python 3 like this:

`$ sudo apt-get install python3 python3-pip`

For other Linux flavors, OS X and Windows, packages are available at:

[http://www.python.org/getit/](http://www.python.org/getit/)

#### 2. Sudoku Solver
To get all of the files needed to run this program, decide for one of the following options and follow it's steps.

##### Using git
1. If the git is not yet installed, check this tutorial how to install it [https://www.atlassian.com/git/tutorials/install-git](https://www.atlassian.com/git/tutorials/install-git)
2. Open the console and go to the directory, where you want to download files.
3. Use the command `git clone https://github.com/ghribar97/Sudoku-Solver.git`.
4. Files are ready. To run Sudoku-Solver check [Quick start](#quick-start).

##### Download files
1. Go to the repository page [https://github.com/ghribar97/Sudoku-Solver](https://github.com/ghribar97/Sudoku-Solver)
2. Click a big green button "Clone or download" and choose "download ZIP" option.
3. After download you must unzip the files with a [WinZip](http://www.winzip.com/win/en/prod_down.html) software, or any other program.
4. Files are ready. To run Sudoku-Solver check [Quick start](#quick-start).

### Quick start

To start a program go to the directory where the Sudoku-Solver files are located and execute this command:

`
$ python3 main.py
`

After the execution the program should start.

## How does it work

Here, we will briefly look at how the program is working - or at least the most important things. For any details please see the code or contact one of the [authors](#authors).

### Extracting Sudoku field

The purpose of this step is to extract the outline of Sudoku field. 
 
Lets first take a look at the image we want to process.

![alt text](SamplePictures/original.jpg?raw=true 'Original picture')

#### Image pre-processing

For smoothing out the noise a bit, lets first blur the image a bit.

```cv2.GaussianBlur(image, (11, 11), 0)```

Where the image is our original photo.

With the noise smoothed out, we can now threshold the image.
The image can have varying illumination levels, so a good choice for a thresholding algorithm would be an adaptive threshold.
It calculates a threshold level several small windows in the image.
This threshold level is calculated using the mean level in the window. So it keeps things illumination independent.

```cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2, dst=image)```

It calculates a mean over a 5x5 window and subtracts 2 from the mean. This is the threshold level for every pixel.

Since we're interested in the borders, and they are black, we invert the image outerBox. Then, the borders of the puzzles are white (along with other noise).

```cv2.bitwise_not(image) ```

This thresholding operation can disconnect certain connected parts (like lines). So dilating the image once will fill up any small "cracks" that might have crept in.

```
kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)
cv2.dilate(image, kernel)
```

Read some more about dilation and erosion: [https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/](https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/)

#### Finding the biggest blob

First, we used the floodfill command. This command returns a bounding rectangle of the pixels it filled. We've assumed the biggest thing in the picture to be the puzzle. So the biggest blob should have be the puzzle.

```area = cv2.floodFill(image, None, (x, y), 64)[0]```

We iterate through the white pixels (>=128) of the image, which ensure that only the white parts are flooded.
Whenever we encounter such a part, we flood it with a dark gray colour (gray level 64). So in the future, we won't be reflooding these blobs.
When we encounter a blob, that has bigger area, than the previous maximum, we have to update maximum and get the point of it.

Now, we have several blobs filled with a dark gray colour (level 64). And we also know the point what produces a blob with maximum area. So we floodfill that point with white:

```cv2.floodFill(image, None, max_point, (255, 255, 255))```

Now, the biggest blob is white. We need to turn the gray color blobs black. We iterate through image again and use this command (if pixel is gray (=64)):

```cv2.floodFill(image, None, (x, y), 0)```

Which will color the blob to black.

Lets see the result now:

![alt text](SamplePictures/blob.jpg?raw=true 'biggest blob')

#### Detecting lines

For detecting lines, we used [Hough Lines](https://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html):

```cv2.HoughLines(image, 1, np.pi / 180, 200)```

Based on each line's rho and theta, we separated them on Horizontals and Verticals. 
For each of them we calculated the intersection point with others.

Now, when we have all of the points, we can get the most top-left, top-right, bottom-left and bottom-right point, that is white (it is on the blob).

#### Result

After we have the corner points, we must calculate the biggest distance between them.
If the difference between distances is to big, we probably did not detect the complete Sudoku field (It should be square). 

The we transformed the perspective to get straight field.

```
src = np.array([tl, tr, bl, br], np.float32)
dst = np.array([(0, 0), (distance-1, 0), (0, distance-1), (distance-1, distance-1)], np.float32)
matrix = cv2.getPerspectiveTransform(src, dst)
cv2.warpPerspective(original_image, matrix, (distance, distance))
```

tl, tr, bl, br are the corners of the biggest blob and the distance is the longest line between points.
Original_image is the picture, taken form the camera, which has not been changed.

Lets see the result:

![alt text](SamplePictures/result.jpg?raw=true 'result')

### Extracting digits

The purpose of this step is to get the digit from an image.

After [Extracting the Sudoku field](#extracting-sudoku-field) we have a clear, straight field, so we can easily divide the field on 81 equal squares.

Like that:

![alt text](SamplePictures/grid.jpg?raw=true 'grid')

We can easily extract the "small square" of the puzzle. Lets take first one for example:

![alt text](SamplePictures/0-original.jpg?raw=true 'first square')

Before continuing with recognition step, we must once again use some image processing.

We use similar technique as in [Image pre-processing](#image-pre-processing). Then we used this command:

```
contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
x, y, width, height = cv2.boundingRect(sorted(contours, key=cv2.contourArea)[-1])
```

Upper function returns the data about the biggest contour in the image (we assume this is the number).
If the ratio between width and height is not good enough, the field does not contain any number.
Otherwise, proceed with processing. Lets see what is the result of the picture now:

![alt text](SamplePictures/0-transform.jpg?raw=true 'transformed first square')

Or a little bit more extreme case:

![alt text](SamplePictures/8-transform.jpg?raw=true 'transformed eight square')

The image still contains a part of the line. So, we had to crop it and extract the contour section.

Last step before recognizing, is to change the image to look more like the images from the training set.
One last time we use:

```cv2.bitwise_not(image)```

to switch white and black pixels. For the end we put this image to a bigger square white image.

The image now, looks like that:

![alt text](SamplePictures/0-result.jpg?raw=true 'result first square')
![alt text](SamplePictures/8-result.jpg?raw=true 'result eight square')

Finally, the image is now ready for recognizing.

## Tests
To run the tests for this project go to [Tests](https://github.com/ghribar97/Sudoku-Solver/tree/master/Tests) directory and run [mainTester.py](https://github.com/ghribar97/Sudoku-Solver/blob/master/Tests/mainTester.py)
Run it with this command:

`$ python3 mainTester.py`

Test coverage is:

[![Coverage Status](https://coveralls.io/repos/github/ghribar97/Sudoku-Solver/badge.svg?branch=master)](https://coveralls.io/github/ghribar97/Sudoku-Solver?branch=master)

## Authors
1. [Alexis Ouksel](https://github.com/AlexOUKS)
2. [Gašper Hribar](https://github.com/ghribar97)
3. [Jesus Prieto Garcia](https://github.com/jesusprietogarcia22)
4. [Roman Suchwalko](https://github.com/rsuchwalko)

[To the top!](#sudoku-solver)
