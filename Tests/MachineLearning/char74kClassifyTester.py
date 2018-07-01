from unittest import TestCase
from MachineLearning.char74kClassify import Char74kClassify
from Common.Errors import InappropriateArgsError

import cv2

class TestChar74kClassify(TestCase):

    def test__resizing(self):
        char74k = Char74kClassify()
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
        expected = cv2.resize(img, (28,28))
        height, width, channels = char74k._resizing(expected).shape
        heightExpected, widthExpected, channelsExpected = char74k._resizing(img).shape
        self.assertEqual([height, width], [heightExpected, widthExpected])

    def test_incorrect__resizing(self):
        char74k = Char74kClassify()
        self.assertRaises(InappropriateArgsError, lambda: char74k._resizing(" "))
        self.assertRaises(InappropriateArgsError, lambda: char74k._resizing(2))
        self.assertRaises(InappropriateArgsError, lambda: char74k._resizing(2.6))

    def test_incorrect__reshaping(self):
        char74k = Char74kClassify()
        self.assertRaises(InappropriateArgsError, lambda: char74k._reshaping(" "))
        self.assertRaises(InappropriateArgsError, lambda: char74k._reshaping(2))
        self.assertRaises(InappropriateArgsError, lambda: char74k._reshaping(2.6))
        self.assertRaises(InappropriateArgsError, lambda: char74k._reshaping([]))

    def test_incorrect__classify_image(self):
        char74k = Char74kClassify()
        self.assertRaises(InappropriateArgsError, lambda: char74k.classify_image(" "))
        self.assertRaises(InappropriateArgsError, lambda: char74k.classify_image(2))
        self.assertRaises(InappropriateArgsError, lambda: char74k.classify_image(2.6))

    def test__load_file_weight(self):
        char74k = Char74kClassify()
        self.assertEqual(char74k._load_file_weight('../../Model/char74k.h5'), True)

    def test__load_model(self):
        char74k = Char74kClassify()
        self.assertEqual(char74k._load_model('../../Model/model.json'), True)

    def test_incorrect__load_model(self):
        char74k = Char74kClassify()
        self.assertRaises(InappropriateArgsError, lambda: char74k._load_model(" "))
        self.assertRaises(InappropriateArgsError, lambda: char74k._load_model(2))
        self.assertRaises(InappropriateArgsError, lambda: char74k._load_model(2.6))

    def test_incorrect__load_file_weight(self):
        char74k = Char74kClassify()
        self.assertRaises(InappropriateArgsError, lambda: char74k._load_file_weight(" "))
        self.assertRaises(InappropriateArgsError, lambda: char74k._load_file_weight(2))
        self.assertRaises(InappropriateArgsError, lambda: char74k._load_file_weight(2.6))

    def test__reshaping(self):
        char74k = Char74kClassify()
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")

        self.assertEqual(char74k._reshaping(char74k._resizing(char74k._img_to_array(img))).shape, (1, 1, 28, 28, 3))


    def test_classify_image(self):
        char74k = Char74kClassify()
        img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
        result = 5

        img = char74k._reshaping(char74k._resizing(char74k._img_to_array(img)))
        self.assertEqual(char74k.classify_image(img), result)
