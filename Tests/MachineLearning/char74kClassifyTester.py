from unittest import TestCase
from MachineLearning.char74kClassify import Char74kClassify
from Common.Errors import InappropriateArgsError
import numpy as np
import cv2

class TestChar74kClassify(TestCase):

    def test__resizing(self):
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
        expected = cv2.resize(img, (28,28))
        char74k = Char74kClassify()

        height, width, channels = char74k._resizing(expected).shape
        heightExpected, widthExpected, channelsExpected = char74k._resizing(img).shape
        self.assertEqual([height, width], [heightExpected, widthExpected])

    def test__load_file_model(self):
        char74k = Char74kClassify()
        self.assertEqual(char74k._load_file_model(), True)

    def test__reshaping(self):
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
        char74k = Char74kClassify()
        self.assertEqual(char74k._reshaping(char74k._resizing(char74k._img_to_array(img))).shape, (1, 1, 28, 28, 3))

    # #
    def test_classify_image(self):
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
        result = 5
        char74k = Char74kClassify()
        img = char74k._reshaping(char74k._resizing(char74k._img_to_array(img)))
        self.assertEqual(char74k.classify_image(img), result)
