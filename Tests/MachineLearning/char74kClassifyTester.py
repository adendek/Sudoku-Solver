from Tests.ImageProcessing.extractSudokuFieldTester import PATH
from MachineLearning.char74kClassify import Char74kClassify
from Common.Errors import InappropriateArgsError
from unittest import TestCase
import cv2


class TestChar74kClassify(TestCase):
    def setUp(self):
        self.char74k = Char74kClassify()
        self.sample_img = cv2.imread(PATH + r"\..\..\SamplePictures\0-result.jpg")
        
    def test__resizing(self):
        expected = cv2.resize(self.sample_img, (28, 28))
        height, width, channels = self.char74k._resizing(expected).shape
        height_expected, width_expected, channels_expected = self.char74k._resizing(self.sample_img).shape
        self.assertEqual([height, width], [height_expected, width_expected])

    def test_incorrect__resizing(self):
        self.assertRaises(InappropriateArgsError, self.char74k._resizing, " ")
        self.assertRaises(InappropriateArgsError, self.char74k._resizing, 2)
        self.assertRaises(InappropriateArgsError, self.char74k._resizing, 2.6)

    def test_incorrect__reshaping(self):
        self.assertRaises(InappropriateArgsError, self.char74k._reshaping, " ")
        self.assertRaises(InappropriateArgsError, self.char74k._reshaping, 2)
        self.assertRaises(InappropriateArgsError, self.char74k._reshaping, 2.6)
        self.assertRaises(InappropriateArgsError, self.char74k._reshaping, [])

    def test_incorrect__classify_image(self):
        self.assertRaises(InappropriateArgsError, self.char74k.classify_image, " ")
        self.assertRaises(InappropriateArgsError, self.char74k.classify_image, 2)
        self.assertRaises(InappropriateArgsError, self.char74k.classify_image, 2.6)

    def test__load_file_weight(self):
        self.assertEqual(self.char74k._load_file_weight(PATH + '/../../Model/char74k.h5'), True)

    def test__load_model(self):
        self.assertEqual(self.char74k._load_model(PATH + '/../../Model/model.json'), True)

    def test_incorrect__load_model(self):
        self.assertRaises(InappropriateArgsError, self.char74k._load_model, " ")
        self.assertRaises(InappropriateArgsError, self.char74k._load_model, 2)
        self.assertRaises(InappropriateArgsError, self.char74k._load_model, 2.6)

    def test_incorrect__load_file_weight(self):
        self.assertRaises(InappropriateArgsError, self.char74k._load_file_weight, " ")
        self.assertRaises(InappropriateArgsError, self.char74k._load_file_weight, 2)
        self.assertRaises(InappropriateArgsError, self.char74k._load_file_weight, 2.6)

    def test__reshaping(self):
        shape = self.char74k._reshaping(self.char74k._resizing(self.char74k._img_to_array(self.sample_img))).shape
        self.assertEqual(shape, (1, 1, 28, 28, 3))

