from unittest import TestCase
from MachineLearning.char74kClassify import Char74kClassify
import numpy as np
import cv2

class TestChar74kClassify(TestCase):
    def test_LoadModel(self):
        pass

    def test_LoadData(self):
        pass

    def test__Resizing(self):
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
        expected = cv2.resize(img, (28,28))
        char74k = Char74kClassify()
        self.assertEqual(char74k._Resizing(img), expected)

    def test__ImgToArray(self):
        img = cv2.imread(
            r"C:\Users\Uporabnik\Desktop\fax\2.Letnik\python\Sudoku-Solver\DataSet\data\Sample004\img004-00002.png")
        expected = np.array(img)
        expected = expected.astype('float32')
        expected /= 255
        char74k = Char74kClassify()
        self.assertEqual(char74k.ImgToArray(img), expected)

    def test__Reshaping(self):
        pass

    def test_ClassifyImage(self):
        img = cv2.imread(
            r"C:\Users\Uporabnik\Desktop\fax\2.Letnik\python\Sudoku-Solver\DataSet\data\Sample004\img004-00002.png")
        result = 5
        char74k = Char74kClassify()
        self.assertEqual(char74k.ClassifyImage(img), result)
