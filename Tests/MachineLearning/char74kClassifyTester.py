from unittest import TestCase
from MachineLearning.char74kClassify import Char74kClassify
from Common.Errors import InappropriateArgsError
import numpy as np
import cv2

class TestChar74kClassify(TestCase):

    def test__Resizing(self):
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
        expected = cv2.resize(img, (28,28))
        char74k = Char74kClassify()

        height, width, channels = char74k._Resizing(expected).shape
        heightExpected, widthExpected, channelsExpected = char74k._Resizing(img).shape
        self.assertEqual([height, width], [heightExpected, widthExpected])

    def test__LoadFileModel(self):
        char74k = Char74kClassify()
        self.assertEqual(char74k._LoadFileModel(), True)

    def test__Reshaping(self):
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
        char74k = Char74kClassify()
        self.assertEqual(char74k._Reshaping(char74k._Resizing(char74k._ImgToArray(img))).shape, (1, 1, 28, 28, 3))

    # #
    # def test_ClassifyImage(self):
    #     img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
    #     result = 5
    #     char74k = Char74kClassify()
    #     img = char74k._Reshaping(char74k._Resizing(char74k._ImgToArray(img)))
    #     self.assertEqual(char74k.ClassifyImage(img), result)
