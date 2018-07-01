from GUI.capureImageView import CaptureImageView, CaptureVideo
from Common.Errors import InappropriateArgsError
from GUI.Framework.widgets import Frame, Button
from unittest import TestCase
import numpy as np
import tkinter


class CaptureImageViewTester(TestCase):
    def setUp(self):
        self.view = CaptureImageView()

    def test_incorrect_handle_errors_at_recognition(self):
        self.assertRaises(InappropriateArgsError, self.view._handle_errors_at_recognition, 1)
        self.assertRaises(InappropriateArgsError, self.view._handle_errors_at_recognition, -1)
        self.assertRaises(InappropriateArgsError, self.view._handle_errors_at_recognition, [1])

    def test_incorrect_handle_image_errors(self):
        self.assertRaises(InappropriateArgsError, self.view._handle_image_errors, 1)
        self.assertRaises(InappropriateArgsError, self.view._handle_image_errors, -1)
        self.assertRaises(InappropriateArgsError, self.view._handle_image_errors, [1])

    def test_get_image(self):
        self.assertEqual(type(self.view._get_image()), np.ndarray)

    def test_load_video(self):
        self.assertEqual(self.view.vid_but.cget("state"), "disabled")
        self.assertEqual(type(self.view.video), CaptureVideo)
        self.assertEqual(self.view.load_from_video, True)

    def test_incorrect_prepare_canvas(self):
        self.assertRaises(InappropriateArgsError, self.view._prepare_canvas, "10", 10)
        self.assertRaises(InappropriateArgsError, self.view._prepare_canvas, 10, "10")
        self.assertRaises(InappropriateArgsError, self.view._prepare_canvas, -10, 10)
        self.assertRaises(InappropriateArgsError, self.view._prepare_canvas, 10, -10)

    def test_correct_prepare_canvas(self):
        canvas = self.view._prepare_canvas(100, 100)
        self.assertEqual(canvas.cget("width"), "100")
        self.assertEqual(canvas.cget("height"), "100")

    def test_incorrect_change_img_size_if_to_big(self):
        self.assertRaises(InappropriateArgsError, self.view._change_img_size_if_to_big, 1)
        self.assertRaises(InappropriateArgsError, self.view._change_img_size_if_to_big, "1")
        self.assertRaises(InappropriateArgsError, self.view._change_img_size_if_to_big, np.ndarray((10, 10)))

    def test_configure_load_from_source_frame(self):
        frame, vid, pic = self.view._configure_load_from_source_frame()
        self.assertEqual(type(frame), Frame)
        self.assertEqual(type(vid), Button)
        self.assertEqual(type(pic), Button)

    def test_init(self):
        self.assertEqual(type(self.view.video), CaptureVideo)
        self.assertEqual(type(self.view.video_delay), int)
        self.assertGreater(self.view.video_delay, 0)
        self.assertEqual(type(self.view.content_frame), Frame)
        self.assertEqual(type(self.view.canvas), tkinter.Canvas)
        self.assertEqual(type(self.view.label_text), str)
        self.assertEqual(type(self.view.load_from_video), bool)
