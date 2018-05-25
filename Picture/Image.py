import cv2
import os


class Image:
    def __init__(self, img_path):

        self.path = img_path
        self.image = cv2.imread(img_path)

