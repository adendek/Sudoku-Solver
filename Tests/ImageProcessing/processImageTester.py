from unittest import TestCase
from ImageProcessing.processImage import ProcessImage
from Common.Errors import InappropriateArgsError
from ImageProcessing.line import Orientation
import numpy as np
import cv2
import os

PATH = os.path.dirname(os.path.realpath(__file__))


class ProcessImageTester(TestCase):
    # missing _image_color and _crop tests
    def test_correct_get_image(self):
        img = cv2.imread(PATH + "/../../SamplePictures/sudokuNice.jpg")
        image = ProcessImage(img)
        squares = image._get_field_squares()
        square = squares[0][0]
        img = image.get_image(square)
        self.assertEqual(type(img), np.ndarray)

    def test_get_field_matrix(self):
        img = cv2.imread(PATH + "/../../SamplePictures/sudokuNice.jpg")
        image = ProcessImage(img)
        field = image.get_field_matrix()
        self.assertEqual(type(field), list)
        self.assertEqual(type(field[0]), list)
        self.assertEqual(len(field), 9)
        self.assertEqual(len(field[0]), 9)

    def test_get_field_squares(self):
        img = cv2.imread(PATH + "/../../SamplePictures/sudokuNice.jpg")
        image = ProcessImage(img)
        self.assertEqual(type(image._get_field_squares()), list)
        self.assertEqual(type(image._get_field_squares()[0]), list)
        self.assertEqual(len(image._get_field_squares()), 9)
        self.assertEqual(len(image._get_field_squares()[0]), 9)

    def test_get_main_lines(self):
        img = cv2.imread(PATH + "/../../SamplePictures/sudokuNice.jpg")
        image = ProcessImage(img)
        all_lines = image._get_all_lines()
        main_lines = image._get_main_lines()
        self.assertGreaterEqual(len(all_lines[Orientation.Vertical]), len(main_lines[Orientation.Vertical]))
        self.assertGreaterEqual(len(all_lines[Orientation.Horizontal]), len(main_lines[Orientation.Horizontal]))
        self.assertEqual(len(main_lines), 2)
        self.assertEqual(type(main_lines), dict)
        first_horiz = main_lines[Orientation.Horizontal][0]
        second_horiz = main_lines[Orientation.Horizontal][1]
        self.assertGreater(second_horiz.y1, first_horiz.y1)
        self.assertGreater(second_horiz.y2, first_horiz.y2)
        first_vert = main_lines[Orientation.Vertical][0]
        second_vert = main_lines[Orientation.Vertical][1]
        self.assertGreater(second_vert.x1, first_vert.x1)
        self.assertGreater(second_vert.x2, first_vert.x2)

    def test_padding(self):
        img = cv2.imread(PATH + "/../../SamplePictures/sudokuNice.jpg")
        image = ProcessImage(img)
        self.assertEqual(image.width // 18, image._get_padding())

    def test_get_all_lines(self):
        img = cv2.imread(PATH + "/../../SamplePictures/sudokuNice.jpg")
        image = ProcessImage(img)
        hough_lines = image._get_hough_lines()
        r = hough_lines[0][0][0]
        theta = hough_lines[0][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * r
        y0 = b * r
        x1 = int(x0 + 1000 * (- b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (- b))
        y2 = int(y0 - 1000 * a)
        line = image._get_all_lines()[Orientation.Vertical][0]
        self.assertEqual((line.x1, line.y1, line.x2, line.y2), (x1, y1, x2, y2))
        self.assertEqual(type(image._get_all_lines()), dict)
        self.assertEqual(len(image._get_all_lines()), 2)

    def test_hough_lines(self):
        img = cv2.imread(PATH + "/../../SamplePictures/sudokuNice.jpg")
        image = ProcessImage(img)
        self.assertEqual(type(image._get_hough_lines()), np.ndarray)

    def test_incorrect_init(self):
        path = "I hope It Doesn't Exists 123890-!"
        self.assertRaises(InappropriateArgsError, lambda: ProcessImage("img"))
        self.assertRaises(InappropriateArgsError, lambda: ProcessImage(1))
        self.assertRaises(FileNotFoundError, lambda: ProcessImage("img", path))
        self.assertRaises(InappropriateArgsError, lambda: ProcessImage("img", 1))

    def test_correct_init(self):
        path = PATH + "/../../SamplePictures/sudokuNice.jpg"
        img = cv2.imread(path)
        image1 = ProcessImage(img)
        image2 = ProcessImage("Doesn't matter", path=path)
        image3 = ProcessImage(img, path)
        self.assertEqual(img.shape, image1.img.shape)  # compare images
        self.assertEqual(np.bitwise_xor(img, image1.img).any(), False)  # compares if they are the same
        self.assertEqual(img.shape, image2.img.shape)
        self.assertEqual(np.bitwise_xor(img, image2.img).any(), False)
        self.assertEqual(img.shape, image3.img.shape)
        self.assertEqual(np.bitwise_xor(img, image3.img).any(), False)
        self.assertEqual((image1.height, image1.width, image1.channels), img.shape)
        self.assertEqual((image2.height, image2.width, image2.channels), img.shape)
        self.assertEqual((image3.height, image3.width, image3.channels), img.shape)
        self.assertEqual(type(image1.grid_lines), dict)
        self.assertEqual(type(image2.grid_lines), dict)
        self.assertEqual(type(image3.grid_lines), dict)
        self.assertEqual(type(image1.squares), list)
        self.assertEqual(type(image2.squares), list)
        self.assertEqual(type(image3.squares), list)
