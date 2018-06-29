from GUI.capureImageView import CaptureVideo
from unittest import TestCase
import numpy as np
import cv2


class CaptureVideoTester(TestCase):
    def setUp(self):
        self.video = CaptureVideo()

    def test_get_image(self):
        img = self.video.get_image()
        self.assertEqual(np.ndarray, type(img))
        self.video.__del__()
        self.assertEqual(self.video.get_image(), None)

    def test_get_frame(self):
        ret, img = self.video.get_frame()
        self.assertEqual(ret, True)
        self.assertEqual(np.ndarray, type(img))
        self.video.__del__()
        ret, img = self.video.get_frame()
        self.assertEqual(ret, None)
        self.assertEqual(img, None)

    def test_del(self):
        before = self.video.video.isOpened()
        self.video.__del__()
        after = self.video.video.isOpened()
        self.assertNotEqual(before, after)

    def test_init(self):
        self.assertEqual(self.video.video_source, 0)
        self.assertEqual(type(self.video.video), type(cv2.VideoCapture()))
        self.assertEqual(self.video.width, self.video.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.assertEqual(self.video.height, self.video.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
